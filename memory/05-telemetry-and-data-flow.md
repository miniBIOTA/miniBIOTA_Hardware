---
id: hardware_telemetry_data_flow
title: Telemetry And Data Flow
domain: engineering_and_hardware
last_updated: 2026-05-11
tags: [memory, telemetry, mqtt, supabase, app, website, wyse]
---
# Telemetry And Data Flow

Telemetry starts on the ESP32 nodes, moves through local MQTT, appears in the App Monitoring tab, and is bridged to Supabase and the public website through the Wyse coordinator.

## Current Flow

```text
ESP32 sensor nodes
  -> Mosquitto on Dell Wyse 3040
  -> App Monitoring tab over direct MQTT
  -> Wyse telemetry coordinator
  -> Supabase telemetry_snapshot row id=1
  -> public website live monitoring
```

The App Monitoring tab is live and display-focused. Biomes 2-5 report sensor data; biome 1 has no sensors; biome 6 is wave-motor-only.

## Coordinator Flow

`services/telemetry_coordinator.py` is the read-only Wyse-side producer:

- Subscribes to local MQTT telemetry/status topics.
- Maintains the latest valid sensor state for biomes 2-5.
- Builds a website-compatible `telemetry_snapshot` payload.
- Upserts Supabase `telemetry_snapshot` row `id=1` every 15 seconds when configured.
- Normalizes placeholder `target_t` values of `0.0` to JSON `null` so the public website does not render an unset target as a real setpoint.
- Can write a local JSON snapshot for development/debugging.
- Does not insert history rows yet.
- Does not poll setpoint commands yet.
- Does not publish MQTT setpoints, pump commands, actuator commands, lighting commands, OTA commands, or firmware updates.

## Wyse Deployment State

As of 2026-05-11, the Wyse coordinator is deployed and running on the Dell Wyse 3040:

- Host/IP: `wyse3040` / `192.168.8.228`.
- SSH: enabled for `minibiota` with a dedicated key from Josue's PC.
- Mosquitto: active and listening on `0.0.0.0:1883`.
- Coordinator location: `~/miniBIOTA_Hardware/services/telemetry_coordinator.py`.
- Python environment: `~/telemetry-venv`.
- Environment file: `~/telemetry.env`, mode `600`, containing Supabase URL/secret and coordinator settings.
- Service: `~/.config/systemd/user/minibiota-telemetry.service`.
- Boot persistence: `loginctl enable-linger minibiota` is enabled.
- Local debug snapshot: `/tmp/minibiota-telemetry-snapshot.json`.

Verified on 2026-05-11:

- Read-only MQTT subscription received live JSON telemetry from sensor biomes.
- Coordinator tests passed on the Wyse.
- Live local snapshot showed biomes 2-5 healthy.
- Supabase accepted `telemetry_snapshot` upserts with `HTTP/2 201 Created` for initial row creation and repeated `HTTP/2 200 OK` updates.

## Planned Structured Tables

- `telemetry_snapshot`: singleton current-state payload for website monitoring.
- `biome_telemetry`: future historical time-series log.
- `setpoint_commands`: future audited command queue for app/web fallback control.

Schema creation or changes require explicit approval.

## Public Website Boundary

The website should read public-safe telemetry from Supabase snapshots/history. Operator-only details such as liquid temperature, pump percentage, and command queues should stay in App/operator surfaces unless explicitly approved for public exposure.

## Verification

For coordinator work, prefer:

- `python -m unittest discover services/tests`
- `python services/telemetry_coordinator.py --dry-run`
- Local snapshot output when useful

MQTT publishes, Supabase schema changes, and service deployment remain separate approval-gated actions.

## Exact References

Use `skills/telemetry-coordinator/reference/telemetry-pipeline-plan.md` for full architecture, topic map, payload contract, planned tables, and phase decisions.
