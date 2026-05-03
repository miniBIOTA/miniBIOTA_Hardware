import json
import os
import sys
import shutil
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from services.telemetry_coordinator import (  # noqa: E402
    LocalSnapshotWriter,
    SupabaseSnapshotWriter,
    TelemetryState,
    build_sample_snapshot,
)


def payload(**overrides):
    base = {
        "atmo_t": 23.0,
        "atmo_h": 70.0,
        "bio_t": 24.0,
        "bio_h": 72.0,
        "liq_t": 21.0,
        "pump_pct": 50,
        "target_t": 24.5,
    }
    base.update(overrides)
    return json.dumps(base).encode("utf-8")


class FakeUpsert:
    def __init__(self):
        self.row = None
        self.on_conflict = None
        self.executed = False

    def upsert(self, row, on_conflict=None):
        self.row = row
        self.on_conflict = on_conflict
        return self

    def execute(self):
        self.executed = True
        return self


class FakeSupabaseClient:
    def __init__(self):
        self.table_name = None
        self.query = FakeUpsert()

    def table(self, table_name):
        self.table_name = table_name
        return self.query


class TelemetryCoordinatorTest(unittest.TestCase):
    def test_sample_snapshot_contains_website_contract_keys_and_sensor_biomes(self):
        snapshot = build_sample_snapshot()

        self.assertEqual(snapshot["schema_version"], 1)
        for key in ("generated_at", "refresh_interval_seconds", "source", "summary", "coordinator", "upstream", "setpoint_channel", "nodes"):
            self.assertIn(key, snapshot)

        nodes = snapshot["nodes"]
        self.assertEqual([node["id"] for node in nodes], [
            "biome-2-lakeshore",
            "biome-3-lowland-meadow",
            "biome-4-mangrove-forest",
            "biome-5-marine-shore",
        ])
        self.assertTrue(all(node["state"] == "healthy" for node in nodes))
        self.assertEqual(nodes[0]["temperature_c"], 24.1)
        self.assertEqual(nodes[0]["humidity_pct"], 72.3)
        self.assertEqual(snapshot["setpoint_channel"]["state"], "healthy")

    def test_node_aging_marks_stale_and_offline(self):
        now = datetime(2026, 5, 2, 12, 0, 0, tzinfo=timezone.utc)
        state = TelemetryState(
            stale_seconds=20,
            offline_seconds=45,
            upstream_checker=lambda: ("healthy", "ok"),
        )
        state.record_telemetry("miniBIOTA/biome/2/telemetry", payload(), now=now - timedelta(seconds=19))
        state.record_telemetry("miniBIOTA/biome/3/telemetry", payload(), now=now - timedelta(seconds=20))
        state.record_telemetry("miniBIOTA/biome/4/telemetry", payload(), now=now - timedelta(seconds=45))

        snapshot = state.build_snapshot(mqtt_connected=True, now=now)
        node_states = {node["id"]: node["state"] for node in snapshot["nodes"]}

        self.assertEqual(node_states["biome-2-lakeshore"], "healthy")
        self.assertEqual(node_states["biome-3-lowland-meadow"], "stale")
        self.assertEqual(node_states["biome-4-mangrove-forest"], "offline")
        self.assertEqual(node_states["biome-5-marine-shore"], "offline")

    def test_malformed_json_is_ignored_and_previous_valid_state_remains(self):
        now = datetime(2026, 5, 2, 12, 0, 0, tzinfo=timezone.utc)
        state = TelemetryState(upstream_checker=lambda: ("healthy", "ok"))
        topic = "miniBIOTA/biome/2/telemetry"
        self.assertTrue(state.record_telemetry(topic, payload(bio_t=24.2), now=now))
        self.assertFalse(state.record_telemetry(topic, b"{not-json", now=now + timedelta(seconds=1)))

        snapshot = state.build_snapshot(mqtt_connected=True, now=now + timedelta(seconds=1))
        node = snapshot["nodes"][0]

        self.assertEqual(node["temperature_c"], 24.2)
        self.assertEqual(state.malformed_packets, 1)

    def test_bad_numeric_fields_become_null(self):
        now = datetime(2026, 5, 2, 12, 0, 0, tzinfo=timezone.utc)
        state = TelemetryState(upstream_checker=lambda: ("healthy", "ok"))
        state.record_telemetry(
            "miniBIOTA/biome/2/telemetry",
            payload(bio_t="bad", bio_h=float("nan"), target_t="24.5"),
            now=now,
        )

        node = state.build_snapshot(mqtt_connected=True, now=now)["nodes"][0]

        self.assertIsNone(node["temperature_c"])
        self.assertIsNone(node["humidity_pct"])
        self.assertEqual(node["target_temperature_c"], 24.5)

    def test_supabase_writer_upserts_singleton_row(self):
        client = FakeSupabaseClient()
        writer = SupabaseSnapshotWriter(client=client, table_name="telemetry_snapshot", row_id=1)
        snapshot = build_sample_snapshot()

        writer.write(snapshot)

        self.assertEqual(client.table_name, "telemetry_snapshot")
        self.assertEqual(client.query.row["id"], 1)
        self.assertEqual(client.query.row["updated_at"], snapshot["generated_at"])
        self.assertEqual(client.query.row["payload"], snapshot)
        self.assertEqual(client.query.on_conflict, "id")
        self.assertTrue(client.query.executed)

    def test_local_snapshot_writer_writes_atomically_readable_json(self):
        temp_root = ROOT / ".test-tmp-telemetry"
        temp_root.mkdir(parents=True, exist_ok=True)
        temp_dir = temp_root / f"atomic-{os.getpid()}"
        shutil.rmtree(temp_dir, ignore_errors=True)
        temp_dir.mkdir(parents=True, exist_ok=True)
        try:
            target = temp_dir / "snapshot.json"
            snapshot = build_sample_snapshot()

            with patch("services.telemetry_coordinator.os.fsync"):
                LocalSnapshotWriter(target).write(snapshot)

            self.assertTrue(target.exists())
            with target.open("r", encoding="utf-8") as handle:
                written = json.load(handle)
            self.assertEqual(written, snapshot)
            temp_files = [name for name in os.listdir(temp_dir) if name.endswith(".tmp")]
            self.assertEqual(temp_files, [])
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
