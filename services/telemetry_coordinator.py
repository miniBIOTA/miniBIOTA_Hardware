#!/usr/bin/env python3
"""Read-only miniBIOTA telemetry snapshot coordinator.

This service subscribes to local biome MQTT telemetry, keeps the latest valid
sensor-node state in memory, and publishes the website-compatible
telemetry_snapshot singleton. It deliberately does not publish MQTT messages,
poll command queues, or control actuators.
"""

from __future__ import annotations

import argparse
import json
import logging
import math
import os
import signal
import socket
import sys
import threading
import time
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Callable, Dict, Iterable, List, Optional, Tuple


MQTT_TELEMETRY_TOPIC = "miniBIOTA/biome/+/telemetry"
MQTT_STATUS_TOPIC = "miniBIOTA/biome/+/status"
SCHEMA_VERSION = 1

EXPECTED_TELEMETRY_FIELDS = (
    "atmo_t",
    "atmo_h",
    "bio_t",
    "bio_h",
    "liq_t",
    "pump_pct",
    "target_t",
)

SENSOR_BIOMES = {
    2: {"id": "biome-2-lakeshore", "name": "Lakeshore"},
    3: {"id": "biome-3-lowland-meadow", "name": "Lowland Meadow"},
    4: {"id": "biome-4-mangrove-forest", "name": "Mangrove Forest"},
    5: {"id": "biome-5-marine-shore", "name": "Marine Shore"},
}


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def utc_iso(value: Optional[datetime] = None) -> str:
    stamp = value or utc_now()
    if stamp.tzinfo is None:
        stamp = stamp.replace(tzinfo=timezone.utc)
    stamp = stamp.astimezone(timezone.utc).replace(microsecond=0)
    return stamp.isoformat().replace("+00:00", "Z")


def env_int(name: str, default: int, minimum: Optional[int] = None) -> int:
    raw = os.environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        parsed = int(raw)
    except ValueError:
        logging.warning("Invalid integer for %s=%r; using %s", name, raw, default)
        return default
    if minimum is not None and parsed < minimum:
        logging.warning("Invalid integer for %s=%r; using %s", name, raw, default)
        return default
    return parsed


def clean_number(value: Any) -> Optional[float]:
    if value is None or isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        candidate = float(value)
    elif isinstance(value, str):
        stripped = value.strip()
        if not stripped or stripped.lower() in {"null", "none", "nan", "inf", "+inf", "-inf", "infinity"}:
            return None
        try:
            candidate = float(stripped)
        except ValueError:
            return None
    else:
        return None

    if not math.isfinite(candidate):
        return None
    return candidate


def parse_biome_id(topic: str) -> Optional[int]:
    parts = topic.split("/")
    if len(parts) != 4:
        return None
    if parts[0] != "miniBIOTA" or parts[1] != "biome":
        return None
    try:
        return int(parts[2])
    except ValueError:
        return None


def state_to_chip(state: str) -> str:
    return {
        "healthy": "nominal",
        "stale": "stale",
        "offline": "critical",
        "degraded": "warning",
        "warning": "warning",
        "standby": "standby",
        "unknown": "info",
    }.get(state, "info")


def state_label(state: str) -> str:
    return {
        "healthy": "Healthy",
        "stale": "Stale",
        "offline": "Offline",
        "degraded": "Degraded",
        "warning": "Warning",
        "standby": "Standby",
        "unknown": "Unknown",
    }.get(state, "Unknown")


def entity(
    *,
    state: str,
    label: str,
    detail: str,
    last_seen: Optional[datetime] = None,
    **extra: Any,
) -> Dict[str, Any]:
    payload = {
        "state": state,
        "chip_state": state_to_chip(state),
        "status_label": state_label(state),
        "label": label,
        "detail": detail,
        "last_seen": utc_iso(last_seen) if last_seen else None,
    }
    payload.update(extra)
    return payload


@dataclass
class CoordinatorConfig:
    mqtt_host: str = "localhost"
    mqtt_port: int = 1883
    mqtt_username: Optional[str] = None
    mqtt_password: Optional[str] = None
    supabase_url: Optional[str] = None
    supabase_service_role_key: Optional[str] = None
    supabase_table: str = "telemetry_snapshot"
    supabase_row_id: int = 1
    snapshot_path: Optional[Path] = None
    refresh_seconds: int = 15
    stale_seconds: int = 20
    offline_seconds: int = 45
    upstream_check_seconds: int = 60
    log_level: str = "INFO"

    @classmethod
    def from_env(cls) -> "CoordinatorConfig":
        snapshot_path = os.environ.get("MINIBIOTA_TELEMETRY_SNAPSHOT_PATH")
        return cls(
            mqtt_host=os.environ.get("MINIBIOTA_MQTT_HOST", "localhost"),
            mqtt_port=env_int("MINIBIOTA_MQTT_PORT", 1883, minimum=1),
            mqtt_username=os.environ.get("MINIBIOTA_MQTT_USERNAME") or None,
            mqtt_password=os.environ.get("MINIBIOTA_MQTT_PASSWORD") or None,
            supabase_url=os.environ.get("SUPABASE_URL") or None,
            supabase_service_role_key=os.environ.get("SUPABASE_SERVICE_ROLE_KEY") or None,
            supabase_table=os.environ.get("MINIBIOTA_TELEMETRY_SUPABASE_TABLE", "telemetry_snapshot"),
            supabase_row_id=env_int("MINIBIOTA_TELEMETRY_SUPABASE_ROW_ID", 1, minimum=1),
            snapshot_path=Path(snapshot_path).expanduser() if snapshot_path else None,
            refresh_seconds=env_int("MINIBIOTA_TELEMETRY_REFRESH_SECONDS", 15, minimum=5),
            stale_seconds=env_int("MINIBIOTA_TELEMETRY_NODE_STALE_SECONDS", 20, minimum=1),
            offline_seconds=env_int("MINIBIOTA_TELEMETRY_NODE_OFFLINE_SECONDS", 45, minimum=1),
            upstream_check_seconds=env_int("MINIBIOTA_TELEMETRY_UPSTREAM_CHECK_SECONDS", 60, minimum=1),
            log_level=os.environ.get("MINIBIOTA_LOG_LEVEL", "INFO"),
        )


@dataclass
class NodeTelemetry:
    biome_id: int
    received_at: datetime
    values: Dict[str, Optional[float]]


@dataclass
class UpstreamState:
    state: str = "unknown"
    detail: str = "Internet upstream reachability has not been checked yet."
    checked_at: Optional[datetime] = None
    last_healthy_at: Optional[datetime] = None


class TelemetryState:
    def __init__(
        self,
        stale_seconds: int = 20,
        offline_seconds: int = 45,
        upstream_check_seconds: int = 60,
        upstream_checker: Optional[Callable[[], Tuple[str, str]]] = None,
    ) -> None:
        self.stale_after = timedelta(seconds=stale_seconds)
        self.offline_after = timedelta(seconds=offline_seconds)
        self.upstream_check_after = timedelta(seconds=upstream_check_seconds)
        self.upstream_checker = upstream_checker or check_upstream
        self.nodes: Dict[int, NodeTelemetry] = {}
        self.status_messages: Dict[int, Tuple[str, datetime]] = {}
        self.upstream = UpstreamState()
        self.malformed_packets = 0

    def record_status(self, topic: str, payload: bytes, now: Optional[datetime] = None) -> bool:
        biome_id = parse_biome_id(topic)
        if biome_id not in SENSOR_BIOMES:
            return False
        stamp = now or utc_now()
        status_text = payload.decode("utf-8", errors="replace").strip()
        self.status_messages[biome_id] = (status_text, stamp)
        return True

    def record_telemetry(self, topic: str, payload: bytes, now: Optional[datetime] = None) -> bool:
        biome_id = parse_biome_id(topic)
        if biome_id not in SENSOR_BIOMES:
            return False

        try:
            decoded = payload.decode("utf-8")
            raw = json.loads(decoded)
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            self.malformed_packets += 1
            logging.warning("Ignoring malformed telemetry on %s: %s", topic, exc)
            return False

        if not isinstance(raw, dict):
            self.malformed_packets += 1
            logging.warning("Ignoring non-object telemetry on %s", topic)
            return False

        values = {field_name: clean_number(raw.get(field_name)) for field_name in EXPECTED_TELEMETRY_FIELDS}
        self.nodes[biome_id] = NodeTelemetry(
            biome_id=biome_id,
            received_at=now or utc_now(),
            values=values,
        )
        return True

    def _node_state(self, record: Optional[NodeTelemetry], now: datetime) -> Tuple[str, str]:
        if record is None:
            return "offline", "No valid telemetry has been received for this sensor node."
        age = now - record.received_at
        age_seconds = int(age.total_seconds())
        if age >= self.offline_after:
            return "offline", f"Latest valid telemetry is {age_seconds}s old, beyond the offline threshold."
        if age >= self.stale_after:
            return "stale", f"Latest valid telemetry is {age_seconds}s old, beyond the stale threshold."
        return "healthy", "Latest valid telemetry is within the expected publish window."

    def _refresh_upstream(self, now: datetime) -> UpstreamState:
        if self.upstream.checked_at and now - self.upstream.checked_at < self.upstream_check_after:
            return self.upstream

        try:
            state, detail = self.upstream_checker()
        except Exception as exc:  # pragma: no cover - defensive around platform socket behavior
            state = "degraded"
            detail = f"Internet upstream check failed with an unexpected error: {exc}"

        state = state if state in {"healthy", "offline", "degraded"} else "degraded"
        self.upstream.state = state
        self.upstream.detail = detail
        self.upstream.checked_at = now
        if state == "healthy":
            self.upstream.last_healthy_at = now
        return self.upstream

    def build_snapshot(self, mqtt_connected: bool, now: Optional[datetime] = None, refresh_seconds: int = 15) -> Dict[str, Any]:
        generated_at = now or utc_now()
        nodes = [self._build_node(biome_id, generated_at) for biome_id in SENSOR_BIOMES]
        coordinator = self._build_coordinator(mqtt_connected=mqtt_connected, nodes=nodes, now=generated_at)
        upstream = self._build_upstream(now=generated_at)
        setpoint_channel = self._build_setpoint_channel(now=generated_at)
        summary = self._build_summary(coordinator=coordinator, upstream=upstream, nodes=nodes)

        return {
            "schema_version": SCHEMA_VERSION,
            "generated_at": utc_iso(generated_at),
            "refresh_interval_seconds": refresh_seconds,
            "source": {
                "kind": "wyse_coordinator",
                "label": "Wyse telemetry coordinator",
                "detail": "Read-only snapshot published from the local MQTT coordinator for sensor biomes 2-5.",
            },
            "summary": summary,
            "coordinator": coordinator,
            "upstream": upstream,
            "setpoint_channel": setpoint_channel,
            "nodes": nodes,
        }

    def _build_node(self, biome_id: int, now: datetime) -> Dict[str, Any]:
        metadata = SENSOR_BIOMES[biome_id]
        record = self.nodes.get(biome_id)
        state, detail = self._node_state(record, now)
        values = record.values if record else {}
        return entity(
            state=state,
            label=f"{metadata['name']} telemetry",
            detail=detail,
            last_seen=record.received_at if record else None,
            id=metadata["id"],
            name=metadata["name"],
            role="Biome Node",
            temperature_c=values.get("bio_t"),
            humidity_pct=values.get("bio_h"),
            target_temperature_c=values.get("target_t"),
        )

    def _build_coordinator(self, mqtt_connected: bool, nodes: List[Dict[str, Any]], now: datetime) -> Dict[str, Any]:
        has_node_data = any(self.nodes.values())
        if mqtt_connected and has_node_data:
            return entity(
                state="healthy",
                label="Coordinator receiving MQTT",
                detail="The coordinator is connected to Mosquitto and has cached sensor-node telemetry.",
                last_seen=now,
            )
        if mqtt_connected:
            return entity(
                state="warning",
                label="Coordinator waiting for telemetry",
                detail="The coordinator is connected to Mosquitto but has not received valid sensor-node telemetry yet.",
                last_seen=now,
            )
        return entity(
            state="degraded",
            label="MQTT disconnected",
            detail="The coordinator is running, but the local Mosquitto connection is currently down.",
            last_seen=now,
        )

    def _build_upstream(self, now: datetime) -> Dict[str, Any]:
        upstream = self._refresh_upstream(now)
        label = {
            "healthy": "Internet upstream reachable",
            "offline": "Internet upstream offline",
            "degraded": "Internet upstream degraded",
        }.get(upstream.state, "Internet upstream unknown")
        return entity(
            state=upstream.state,
            label=label,
            detail=upstream.detail,
            last_seen=upstream.last_healthy_at or upstream.checked_at,
        )

    def _build_setpoint_channel(self, now: datetime) -> Dict[str, Any]:
        recent_targets: List[Tuple[datetime, float]] = []
        for record in self.nodes.values():
            target = record.values.get("target_t")
            if target is not None and now - record.received_at < self.offline_after:
                recent_targets.append((record.received_at, target))

        if not recent_targets:
            return entity(
                state="standby",
                label="Target temperatures not visible yet",
                detail="No recent telemetry with target_t has been received. The website remains read-only.",
                last_seen=None,
                target_temperature_c=None,
            )

        last_seen, target = max(recent_targets, key=lambda item: item[0])
        return entity(
            state="healthy",
            label="Target temperatures visible",
            detail="Recent telemetry includes target_t values as read-only website data.",
            last_seen=last_seen,
            target_temperature_c=target,
        )

    def _build_summary(
        self,
        coordinator: Dict[str, Any],
        upstream: Dict[str, Any],
        nodes: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        counts = {
            "healthy_nodes": sum(1 for node in nodes if node["state"] == "healthy"),
            "stale_nodes": sum(1 for node in nodes if node["state"] == "stale"),
            "offline_nodes": sum(1 for node in nodes if node["state"] == "offline"),
            "total_nodes": len(nodes),
        }

        if coordinator["state"] in {"degraded", "warning"}:
            state = "warning"
            label = "Telemetry coordinator is degraded"
            detail = "The snapshot producer is running, but the local MQTT feed is disconnected or still waiting for node data."
        elif counts["offline_nodes"] or counts["stale_nodes"]:
            state = "warning"
            label = "Telemetry is partially degraded"
            detail = "The coordinator is publishing snapshots, but one or more sensor nodes are stale or offline."
        elif upstream["state"] in {"offline", "degraded"}:
            state = "warning"
            label = "Telemetry upstream is degraded"
            detail = "Local MQTT telemetry is fresh, but the internet upstream check is not healthy."
        else:
            state = "healthy"
            label = "Telemetry surface is healthy"
            detail = "The coordinator, upstream check, and sensor-node heartbeats are all healthy."

        payload = entity(state=state, label=label, detail=detail)
        payload.update(counts)
        return payload


def check_upstream(host: str = "1.1.1.1", port: int = 53, timeout: float = 3.0) -> Tuple[str, str]:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return "healthy", "A lightweight TCP reachability check to the public internet succeeded."
    except OSError as exc:
        return "offline", f"A lightweight TCP reachability check to the public internet failed: {exc}"


class LocalSnapshotWriter:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, snapshot: Dict[str, Any]) -> None:
        target = self.path
        target.parent.mkdir(parents=True, exist_ok=True)
        temp_path = self._temp_path(target)
        try:
            with temp_path.open("x", encoding="utf-8") as handle:
                json.dump(snapshot, handle, indent=2, sort_keys=True, allow_nan=False)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temp_path, target)
        finally:
            if temp_path and temp_path.exists():
                try:
                    temp_path.unlink()
                except OSError:
                    logging.debug("Unable to remove temporary snapshot file %s", temp_path)

    def _temp_path(self, target: Path) -> Path:
        thread_id = threading.get_ident()
        for attempt in range(100):
            candidate = target.with_name(f".{target.name}.{os.getpid()}.{thread_id}.{attempt}.tmp")
            if not candidate.exists():
                return candidate
        raise FileExistsError(f"Unable to allocate temporary snapshot path beside {target}")


class SupabaseSnapshotWriter:
    def __init__(self, client: Any, table_name: str, row_id: int) -> None:
        self.client = client
        self.table_name = table_name
        self.row_id = row_id

    @classmethod
    def from_config(cls, config: CoordinatorConfig) -> Optional["SupabaseSnapshotWriter"]:
        if not config.supabase_url or not config.supabase_service_role_key:
            missing = []
            if not config.supabase_url:
                missing.append("SUPABASE_URL")
            if not config.supabase_service_role_key:
                missing.append("SUPABASE_SERVICE_ROLE_KEY")
            logging.warning("Supabase writer disabled; missing %s", ", ".join(missing))
            return None

        try:
            from supabase import create_client
        except ImportError:
            logging.warning("Supabase writer disabled; install the supabase package to enable it")
            return None

        client = create_client(config.supabase_url, config.supabase_service_role_key)
        return cls(client=client, table_name=config.supabase_table, row_id=config.supabase_row_id)

    def write(self, snapshot: Dict[str, Any]) -> None:
        row = {
            "id": self.row_id,
            "updated_at": snapshot["generated_at"],
            "payload": snapshot,
        }
        self.client.table(self.table_name).upsert(row, on_conflict="id").execute()


class CoordinatorService:
    def __init__(self, config: CoordinatorConfig) -> None:
        self.config = config
        self.state = TelemetryState(
            stale_seconds=config.stale_seconds,
            offline_seconds=config.offline_seconds,
            upstream_check_seconds=config.upstream_check_seconds,
        )
        self.mqtt_connected = False
        self.stop_event = threading.Event()
        self.mqtt_client: Any = None
        self.writers = self._build_writers(config)

    def _build_writers(self, config: CoordinatorConfig) -> List[Any]:
        writers: List[Any] = []
        if config.snapshot_path:
            writers.append(LocalSnapshotWriter(config.snapshot_path))

        supabase_writer = SupabaseSnapshotWriter.from_config(config)
        if supabase_writer:
            writers.append(supabase_writer)

        if not writers:
            logging.error(
                "No telemetry output configured. Set SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY, "
                "or MINIBIOTA_TELEMETRY_SNAPSHOT_PATH for local-file/debug mode."
            )
        return writers

    def start(self) -> None:
        self._start_mqtt()
        logging.info("Telemetry coordinator started; refresh=%ss", self.config.refresh_seconds)
        try:
            while not self.stop_event.is_set():
                self.publish_once()
                self.stop_event.wait(self.config.refresh_seconds)
        finally:
            self.stop()

    def stop(self) -> None:
        self.stop_event.set()
        if self.mqtt_client is not None:
            try:
                self.mqtt_client.loop_stop()
                self.mqtt_client.disconnect()
            except Exception as exc:  # pragma: no cover - cleanup should never mask shutdown
                logging.debug("MQTT cleanup failed: %s", exc)

    def publish_once(self) -> Dict[str, Any]:
        snapshot = self.state.build_snapshot(
            mqtt_connected=self.mqtt_connected,
            refresh_seconds=self.config.refresh_seconds,
        )
        for writer in self.writers:
            try:
                writer.write(snapshot)
            except Exception as exc:
                logging.warning("Telemetry snapshot write failed for %s: %s", writer.__class__.__name__, exc)
        return snapshot

    def _start_mqtt(self) -> None:
        try:
            import paho.mqtt.client as mqtt
        except ImportError:
            logging.warning("MQTT disabled; install paho-mqtt to subscribe to local telemetry")
            return

        client_id = f"minibiota-telemetry-coordinator-{os.getpid()}"
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id=client_id)
        except AttributeError:
            client = mqtt.Client(client_id=client_id)

        if self.config.mqtt_username:
            client.username_pw_set(self.config.mqtt_username, self.config.mqtt_password)

        client.on_connect = self._on_mqtt_connect
        client.on_disconnect = self._on_mqtt_disconnect
        client.on_message = self._on_mqtt_message
        client.reconnect_delay_set(min_delay=1, max_delay=30)
        client.connect_async(self.config.mqtt_host, self.config.mqtt_port, keepalive=30)
        client.loop_start()
        self.mqtt_client = client

    def _on_mqtt_connect(self, client: Any, userdata: Any, flags: Any, reason_code: Any, properties: Any = None) -> None:
        rc = mqtt_reason_code(reason_code)
        if rc == 0:
            self.mqtt_connected = True
            client.subscribe([(MQTT_TELEMETRY_TOPIC, 0), (MQTT_STATUS_TOPIC, 0)])
            logging.info("Connected to MQTT broker and subscribed to telemetry/status topics")
        else:
            self.mqtt_connected = False
            logging.warning("MQTT connection failed with code %s", reason_code)

    def _on_mqtt_disconnect(self, client: Any, userdata: Any, *args: Any) -> None:
        self.mqtt_connected = False
        logging.warning("MQTT disconnected; coordinator will keep publishing aged cache snapshots")

    def _on_mqtt_message(self, client: Any, userdata: Any, message: Any) -> None:
        topic = getattr(message, "topic", "")
        payload = getattr(message, "payload", b"")
        if topic.endswith("/telemetry"):
            self.state.record_telemetry(topic, payload)
        elif topic.endswith("/status"):
            self.state.record_status(topic, payload)


def mqtt_reason_code(reason_code: Any) -> int:
    if isinstance(reason_code, int):
        return reason_code
    value = getattr(reason_code, "value", None)
    if isinstance(value, int):
        return value
    try:
        return int(reason_code)
    except (TypeError, ValueError):
        return 0 if str(reason_code).lower() in {"success", "normal disconnection"} else -1


def sample_payloads() -> Iterable[Tuple[str, bytes]]:
    samples = {
        2: {"atmo_t": 23.8, "atmo_h": 70.2, "bio_t": 24.1, "bio_h": 72.3, "liq_t": 21.0, "pump_pct": 45, "target_t": 24.5},
        3: {"atmo_t": 24.0, "atmo_h": 68.9, "bio_t": 24.3, "bio_h": 69.5, "liq_t": None, "pump_pct": 40, "target_t": 24.5},
        4: {"atmo_t": 25.1, "atmo_h": 81.0, "bio_t": 25.4, "bio_h": 83.1, "liq_t": 22.2, "pump_pct": 55, "target_t": 25.0},
        5: {"atmo_t": 24.7, "atmo_h": 76.4, "bio_t": 24.9, "bio_h": 78.2, "liq_t": 22.8, "pump_pct": 50, "target_t": 25.0},
    }
    for biome_id, payload in samples.items():
        yield f"miniBIOTA/biome/{biome_id}/telemetry", json.dumps(payload).encode("utf-8")


def build_sample_snapshot(refresh_seconds: int = 15) -> Dict[str, Any]:
    state = TelemetryState(upstream_checker=lambda: ("healthy", "Dry-run upstream check skipped; sample snapshot marked healthy."))
    now = utc_now()
    for topic, payload in sample_payloads():
        state.record_telemetry(topic, payload, now=now)
    return state.build_snapshot(mqtt_connected=True, now=now, refresh_seconds=refresh_seconds)


def configure_logging(level_name: str) -> None:
    level = getattr(logging, level_name.upper(), logging.INFO)
    logging.basicConfig(
        level=level,
        format="%(asctime)s %(levelname)s %(message)s",
    )


def parse_args(argv: Optional[List[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="miniBIOTA read-only telemetry snapshot coordinator")
    parser.add_argument("--dry-run", action="store_true", help="Print a sample website-compatible snapshot and exit")
    parser.add_argument("--snapshot-path", help="Override MINIBIOTA_TELEMETRY_SNAPSHOT_PATH")
    parser.add_argument("--log-level", help="Override MINIBIOTA_LOG_LEVEL")
    return parser.parse_args(argv)


def main(argv: Optional[List[str]] = None) -> int:
    args = parse_args(argv)
    config = CoordinatorConfig.from_env()
    if args.snapshot_path:
        config.snapshot_path = Path(args.snapshot_path).expanduser()
    if args.log_level:
        config.log_level = args.log_level
    configure_logging(config.log_level)

    if args.dry_run:
        snapshot = build_sample_snapshot(refresh_seconds=config.refresh_seconds)
        if config.snapshot_path:
            LocalSnapshotWriter(config.snapshot_path).write(snapshot)
            logging.info("Wrote dry-run snapshot to %s", config.snapshot_path)
        print(json.dumps(snapshot, indent=2, sort_keys=True, allow_nan=False))
        return 0

    service = CoordinatorService(config)

    def _handle_signal(signum: int, frame: Any) -> None:
        logging.info("Received signal %s; stopping telemetry coordinator", signum)
        service.stop()

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)
    service.start()
    return 0


if __name__ == "__main__":
    sys.exit(main())
