---
id: telemetry_pipeline_plan_reference
title: Telemetry Pipeline Plan
domain: engineering_and_hardware
last_updated: 2026-05-11
status: snapshot-producer-deployed
tags: [telemetry, mqtt, supabase, wyse, app, website, pipeline]
---
# Telemetry Pipeline Plan

## Goal

Wire live ESP32 sensor data from the local biome network to three surfaces:

- App: full operator view with real-time readings and future setpoint control.
- Railway website: public read-only monitoring surface with historical charts.
- Supabase: historical time-series log for biome telemetry.

## Current Implementation Slice

The first Wyse-side producer implementation is intentionally read-only and limited to the website-compatible `telemetry_snapshot` singleton. It subscribes to local MQTT telemetry/status topics, maintains latest valid state for sensor biomes 2-5, upserts `telemetry_snapshot` row `id=1`, and can optionally write the same snapshot to a local JSON file for development/debug use.

Deployment status as of 2026-05-11: the coordinator is running on the Dell Wyse 3040 as the `minibiota` user service `minibiota-telemetry.service`, with systemd user linger enabled so it can start without an interactive login.

Deferred from this first pass:

- `biome_telemetry` history inserts.
- `setpoint_commands` polling.
- MQTT setpoint publishing.
- Pump, actuator, lighting, OTA, or other control commands.

## Architecture Overview

```text
ESP32 nodes
  publish every 10s to MQTT topics
  -> Mosquitto broker on Dell Wyse 3040 at 192.168.8.228:1883
     -> Wyse coordinator service
        -> every 15s upserts telemetry_snapshot for website reads
        -> future: every 60s inserts biome_telemetry rows
        -> future: polls setpoint_commands and publishes to MQTT
     -> App Monitoring tab
        -> subscribes directly to MQTT for live display
        -> future: publishes setpoints directly to MQTT when approved
        -> future: falls back to telemetry_snapshot when off mB2.4
Supabase
  -> telemetry_snapshot
  -> biome_telemetry
  -> setpoint_commands
Railway website
  -> reads telemetry_snapshot from Supabase
```

## MQTT Topic Map

| Biome | biome_id | MQTT topic prefix | OTA hostname |
|---|---:|---|---|
| Freshwater Lake | 1 | `miniBIOTA/biome/1/` | `biome1-lake` |
| Lakeshore | 2 | `miniBIOTA/biome/2/` | `biome2-lakeshore` |
| Lowland Meadow | 3 | `miniBIOTA/biome/3/` | `biome3-meadow` |
| Mangrove Forest | 4 | `miniBIOTA/biome/4/` | `biome4-mangrove` |
| Marine Shore | 5 | `miniBIOTA/biome/5/` | `biome5-marine` |
| Seagrass Meadow | 6 | `miniBIOTA/biome/6/` | `biome6-seagrass` |

Each biome publishes or uses:

- `.../telemetry`: JSON telemetry every 10 seconds where sensors exist.
- `.../status`: `"online"` on connect.
- `.../setpoint`: incoming target temperature float string.

## Supabase Tables

### `biome_telemetry`

Future time-series log. Wyse writes one row per active biome per minute.

| Column | Type | Notes |
|---|---|---|
| `id` | bigserial | Primary key |
| `biome_id` | integer | 1-6, references biomes |
| `recorded_at` | timestamptz | Timestamp of the sample |
| `bio_temp_c` | float | Biome air temperature |
| `bio_humidity_pct` | float | Biome air humidity |
| `atmo_temp_c` | float | Atmosphere air temperature |
| `atmo_humidity_pct` | float | Atmosphere air humidity |
| `liquid_temp_c` | float | Coolant/heat exchanger temp, nullable |
| `pump_pct` | integer | Pump output 0-100%, nullable |
| `target_temp_c` | float | Active setpoint at time of sample |

Public website reads only `bio_temp_c`, `bio_humidity_pct`, `atmo_temp_c`, and `atmo_humidity_pct`. App/operator surfaces can read liquid temperature and pump percent.

### `telemetry_snapshot`

Singleton. Wyse upserts one row, `id=1`, every 15 seconds. Website reads it for live monitoring.

| Column | Type | Notes |
|---|---|---|
| `id` | integer | Always 1 |
| `updated_at` | timestamptz | Last Wyse write time |
| `payload` | JSONB | Full website contract shape |

Payload includes schema version, coordinator, upstream, setpoint channel, summary, and nodes.

Target/setpoint semantics:

- Real configured/known setpoint: numeric `target_temperature_c`.
- No configured/known setpoint: `target_temperature_c: null`.
- Firmware placeholder `target_t: 0.0` must be normalized by the coordinator to `null` before publishing the website snapshot.

Node entry shape:

```json
{
  "id": "biome-2-lakeshore",
  "name": "Lakeshore",
  "role": "Biome Node",
  "state": "healthy",
  "temperature_c": 24.5,
  "humidity_pct": 65.2,
  "target_temperature_c": null
}
```

### `setpoint_commands`

Future command queue for setpoint and future parameter changes.

| Column | Type | Notes |
|---|---|---|
| `id` | bigserial | Primary key |
| `biome_id` | integer | 1-6 |
| `target_temp_c` | float | New target temperature |
| `created_at` | timestamptz | When the command was queued |
| `status` | text | `pending`, `published`, or `error` |
| `published_at` | timestamptz | When Wyse published it to MQTT |

Setpoint queue processing is not active in the first read-only coordinator implementation.

## Component Build Plan

### Phase 1 - Supabase Schema

- Create `biome_telemetry`, `telemetry_snapshot`, and `setpoint_commands`.
- Add RLS: public read-only for telemetry tables, service-role only for command queue.

Schema work requires explicit approval.

### Phase 2 - Wyse Coordinator Service

Current file: `services/telemetry_coordinator.py`.

Logic:

- Connect to Mosquitto at localhost on the Wyse.
- Subscribe to `miniBIOTA/biome/+/telemetry` and `miniBIOTA/biome/+/status`.
- Maintain in-memory latest state by biome ID.
- Every 15 seconds build snapshot payload and upsert `telemetry_snapshot` id 1 when Supabase is configured.
- Optionally write local JSON snapshot.

Deployment reference:

- `deploy/systemd/minibiota-telemetry.service.example`
- Service should start on boot and restart on crash.

Current Wyse deployment:

- Host/IP: `wyse3040` / `192.168.8.228`.
- SSH: `minibiota@192.168.8.228` with Josue PC key `C:\Users\gimbo\.ssh\minibiota_wyse_ed25519`.
- Runtime directory: `/home/minibiota/miniBIOTA_Hardware`.
- Virtualenv: `/home/minibiota/telemetry-venv`.
- Env file: `/home/minibiota/telemetry.env`, mode `600`.
- User service: `/home/minibiota/.config/systemd/user/minibiota-telemetry.service`.
- Local debug snapshot: `/tmp/minibiota-telemetry-snapshot.json`.
- Verified writes: Supabase `telemetry_snapshot` row `id=1` received initial `HTTP/2 201 Created` and ongoing `HTTP/2 200 OK` upserts on 2026-05-11.

### Phase 3 - Website Update

Website should replace file-based local telemetry snapshots with Supabase reads from `telemetry_snapshot` id 1, then fall back to placeholder payload if missing or stale.

### Phase 4 - App Monitoring Complete 2026-04-25

Implemented in the App:

- MQTT-only connection to `192.168.8.228:1883`.
- Connection banner.
- Six biome subtabs.
- Seven sensor fields where applicable.
- Healthy/stale/offline chip status.
- Setpoint controls deferred.

Key gotcha resolved: firmware emitted `nan` for missing sensors. App parsing requires valid JSON, so firmware now emits `null`.

Remaining from original Phase 4 spec:

- Setpoint control per biome.
- Supabase fallback when off `mB2.4`.

## Decisions Made

| Decision | Choice | Reason |
|---|---|---|
| Telemetry sampling rate for Supabase history | 1 minute | 10 seconds is more resolution than history needs |
| Snapshot refresh rate | 15 seconds | Matches website live monitoring needs |
| Snapshot delivery to website | Supabase | Railway cannot read local files from the Windows machine |
| Two-way control path | Direct MQTT from app plus future Supabase command queue | Instant control locally, audited fallback remotely |
| Wyse as always-on aggregator | Yes | Website needs data even when App is closed |
| Public telemetry fields | Bio/atmo temp and humidity | Liquid temp and pump percent are operator-only |
| Monitoring tab location | App Monitoring tab | Dedicated operator surface |

## Open Items

- Confirm Python/runtime environment on the Wyse for deployment.
- Decide whether `setpoint_commands` stays temperature-only or accepts future parameters.
- Decide retention policy for `biome_telemetry`, likely 90-day rolling delete.
