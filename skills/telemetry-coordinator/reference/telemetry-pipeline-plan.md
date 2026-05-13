---
id: telemetry_pipeline_plan_reference
title: Telemetry Pipeline Plan
domain: engineering_and_hardware
last_updated: 2026-05-13
status: snapshot-and-history-producer-deployed
tags: [telemetry, mqtt, supabase, wyse, app, website, pipeline]
---
# Telemetry Pipeline Plan

## Goal

Wire live ESP32 sensor data from the local biome network to three surfaces:

- App: full operator view with real-time readings and future setpoint control.
- Railway website: public read-only monitoring surface with historical charts.
- Supabase: historical time-series log for biome telemetry.

## Current Implementation Slice

The Wyse-side producer implementation is intentionally read-only. It subscribes to local MQTT telemetry/status topics, maintains latest valid state for sensor biomes 2-5, upserts the website-compatible `telemetry_snapshot` row `id=1`, writes internal `biome_telemetry` history rows for analysis, and can optionally write the same snapshot to a local JSON file for development/debug use.

Deployment status as of 2026-05-13: the coordinator is running on the Dell Wyse 3040 as the `minibiota` user service `minibiota-telemetry.service`, with systemd user linger enabled so it can start without an interactive login. It publishes the public `telemetry_snapshot` and writes internal `biome_telemetry` history.

Deferred from this first pass:

- `setpoint_commands` polling.
- MQTT setpoint publishing.
- Pump, actuator, lighting, OTA, or other control commands.

Completed 2026-05-13:

- `biome_telemetry` internal history for sensor biomes 2-5, sampled by the Wyse coordinator about once per minute. This stores biome air, atmosphere air, liquid/heat-exchanger temperature, pump percentage, and target temperature for analysis. It is not part of the public website snapshot contract.

## Architecture Overview

```text
ESP32 nodes
  publish every 10s to MQTT topics
  -> Mosquitto broker on Dell Wyse 3040 at 192.168.8.228:1883
     -> Wyse coordinator service
        -> every 15s upserts telemetry_snapshot for website reads
        -> every 60s inserts biome_telemetry rows for internal analysis
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

Internal time-series log. Wyse writes one row per active sensor biome per minute. Schema packet applied 2026-05-13: `services/schema/biome_telemetry_schema_2026-05-13.sql`.

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
| `pump_pct` | float | Pump output 0-100%, nullable |
| `target_temp_c` | float | Active setpoint at time of sample |

Public website reads only explicitly approved public-safe fields. App/operator and analysis surfaces can read liquid temperature and pump percent. As of 2026-05-13, liquid/heat-exchanger temperature and pump percent are intended for internal analysis, not public Web display.

### `telemetry_snapshot`

Singleton. Wyse upserts one row, `id=1`, every 15 seconds. Website reads it for live monitoring.

| Column | Type | Notes |
|---|---|---|
| `id` | integer | Always 1 |
| `updated_at` | timestamptz | Last Wyse write time |
| `payload` | JSONB | Full website contract shape |

Payload includes schema version, coordinator, upstream, setpoint channel, summary, and nodes. `payload.nodes` includes both biome nodes and public atmosphere sensor nodes for sensor biomes 2-5.

Target/setpoint semantics:

- Real configured/known setpoint: numeric `target_temperature_c`.
- No configured/known setpoint: `target_temperature_c: null`.
- Firmware placeholder `target_t: 0.0` must be normalized by the coordinator to `null` before publishing the website snapshot.

Biome node entry shape:

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

Atmosphere sensor node entry shape:

```json
{
  "id": "atmosphere-2-lakeshore",
  "name": "Lakeshore Atmosphere",
  "role": "Atmosphere Sensor",
  "state": "healthy",
  "chip_state": "nominal",
  "status_label": "Healthy",
  "detail": "Latest valid telemetry is within the expected publish window.",
  "last_seen": "2026-05-13T12:00:00Z",
  "temperature_c": 23.8,
  "humidity_pct": 70.2,
  "target_temperature_c": null
}
```

Current public atmosphere node IDs:

- `atmosphere-2-lakeshore`
- `atmosphere-3-lowland-meadow`
- `atmosphere-4-mangrove-forest`
- `atmosphere-5-marine-shore`

Public node payloads must not include liquid temperature, pump percentage, relay, command queue, actuator, or other control fields.

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

Current deployed slice:

- `telemetry_snapshot` exists and receives singleton row `id=1` from the Wyse coordinator.
- Website reads are public-safe and read-only through the Supabase snapshot contract.
- `biome_telemetry` exists for internal history and receives Wyse coordinator rows about every minute.

Future schema work:

- Create `setpoint_commands` only when command queues are explicitly scoped.
- Add or adjust RLS for future telemetry/history/command tables as needed; command queues remain service-role only.

Schema work requires explicit approval.

### Phase 2 - Wyse Coordinator Service

Current file: `services/telemetry_coordinator.py`.

Logic:

- Connect to Mosquitto at localhost on the Wyse.
- Subscribe to `miniBIOTA/biome/+/telemetry` and `miniBIOTA/biome/+/status`.
- Maintain in-memory latest state by biome ID.
- Every 15 seconds build snapshot payload and upsert `telemetry_snapshot` id 1 when Supabase is configured.
- Every 60 seconds build internal history rows and upsert `biome_telemetry` by `(biome_id, recorded_at)` when Supabase and the history table are configured.
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
- Verified writes: Supabase `telemetry_snapshot` row `id=1` received ongoing `HTTP/2 200 OK` upserts on 2026-05-13, and `biome_telemetry` received live rows for biomes 2-5 with `liquid_temp_c` and `pump_pct`.

### Phase 3 - Website Update

Website reads from Supabase `telemetry_snapshot` id 1 for live monitoring, then falls back to a placeholder/degraded payload if the row is missing or stale.

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

- Decide whether `setpoint_commands` stays temperature-only or accepts future parameters.
- Decide retention policy for `biome_telemetry`, likely 90-day rolling delete.
