---
id: telemetry_pipeline_plan
title: Telemetry Pipeline — Architecture Plan
domain: engineering_and_hardware
created: 2026-04-24
status: phase-4-complete
tags: [telemetry, mqtt, supabase, wyse, app, website, pipeline]
---

# Telemetry Pipeline — Architecture Plan

## Goal

Wire live ESP32 sensor data from the local biome network to three surfaces:
- **App (Electron):** Full operator view with real-time readings and setpoint control
- **Railway website:** Public read-only monitoring surface with historical charts
- **Supabase:** Historical time-series log for all biome telemetry

## Architecture Overview

```
ESP32 nodes (6 biomes)
  │  publish every 10s to MQTT topics
  ▼
Mosquitto broker — Dell Wyse 3040 (192.168.8.228:1883)
  │
  ├── Wyse coordinator service (Python, systemd)
  │     ├── every 15s → upserts telemetry_snapshot (Supabase) ← website reads this
  │     ├── every 60s → inserts biome_telemetry rows (Supabase) ← historical log
  │     └── polls setpoint_commands (Supabase) → publishes to MQTT → ESP32
  │
  └── App Monitoring tab (Electron, when on mB2.4)
        ├── subscribes to MQTT directly → live display (real-time)
        ├── publishes setpoints directly to MQTT → ESP32 (instant)
        └── fallback: reads telemetry_snapshot from Supabase (when off mB2.4)

Supabase
  ├── telemetry_snapshot  ← website reads (current state)
  ├── biome_telemetry     ← historical log (1-min resolution)
  └── setpoint_commands   ← queued commands from app or future web UI

Railway website (utils/telemetry.py)
  └── reads telemetry_snapshot from Supabase
      (replaces MINIBIOTA_TELEMETRY_SNAPSHOT_PATH file-based approach)
```

---

## MQTT Topic Map

| Biome | biome_id | MQTT topic prefix | OTA hostname |
|---|---|---|---|
| Freshwater Lake | 1 | `miniBIOTA/biome/1/` | `biome1-freshwater-lake` |
| Lakeshore | 2 | `miniBIOTA/biome/2/` | `biome2-lakeshore` |
| Lowland Meadow | 3 | `miniBIOTA/biome/3/` | `biome3-lowland-meadow` |
| Mangrove Forest | 4 | `miniBIOTA/biome/4/` | `biome4-mangrove-forest` |
| Marine Shore | 5 | `miniBIOTA/biome/5/` | `biome5-marine-shore` |
| Seagrass Meadow | 6 | `miniBIOTA/biome/6/` | `biome6-seagrass-meadow` |

Each biome publishes three sub-topics:
- `.../telemetry` — `{"atmo_t", "atmo_h", "bio_t", "bio_h", "liq_t", "pump_pct", "target_t"}` every 10s
- `.../status` — `"online"` on connect
- `.../setpoint` — subscribes for incoming target temperature (float string)

---

## Supabase Tables (New)

### `biome_telemetry`
Time-series log. Wyse writes one row per active biome per minute.

| Column | Type | Notes |
|---|---|---|
| `id` | bigserial | Primary key |
| `biome_id` | integer | 1–6, references biomes |
| `recorded_at` | timestamptz | Timestamp of the sample |
| `bio_temp_c` | float | Biome air temperature |
| `bio_humidity_pct` | float | Biome air humidity |
| `atmo_temp_c` | float | Atmosphere air temperature |
| `atmo_humidity_pct` | float | Atmosphere air humidity |
| `liquid_temp_c` | float | Coolant/heat exchanger temp (nullable) |
| `pump_pct` | integer | Pump output 0–100% (nullable) |
| `target_temp_c` | float | Active setpoint at time of sample |

**Public website reads:** `bio_temp_c`, `bio_humidity_pct`, `atmo_temp_c`, `atmo_humidity_pct` only.  
**App reads:** all columns including `liquid_temp_c` and `pump_pct`.

**Estimated volume:** ~8,640 rows/day across 6 biomes. Plan a 90-day retention cleanup job before year-end.

### `telemetry_snapshot`
Singleton. Wyse upserts one row (id=1) every 15s. Website reads it for `/live-monitoring`.

| Column | Type | Notes |
|---|---|---|
| `id` | integer | Always 1 (singleton) |
| `updated_at` | timestamptz | Last Wyse write time |
| `payload` | JSONB | Full website contract shape (schema_version, coordinator, upstream, setpoint_channel, nodes) |

The `payload` JSONB must match the existing website contract defined in `miniBIOTA_Web/docs/technical_architecture.md` section 4.6.

Nodes array maps biome_id → node entry:
```json
{
  "id": "biome-2-lakeshore",
  "name": "Lakeshore",
  "role": "Biome Node",
  "state": "healthy",
  "temperature_c": <bio_temp_c>,
  "humidity_pct": <bio_humidity_pct>,
  "target_temperature_c": <target_t>
}
```

### `setpoint_commands`
Command queue for setpoint and future parameter changes.

| Column | Type | Notes |
|---|---|---|
| `id` | bigserial | Primary key |
| `biome_id` | integer | 1–6 |
| `target_temp_c` | float | New target temperature |
| `created_at` | timestamptz | When the command was queued |
| `status` | text | `pending` → `published` or `error` |
| `published_at` | timestamptz | When Wyse published it to MQTT (nullable) |

Wyse polls this table every 5–10s, picks up `status='pending'` rows, publishes to MQTT, then sets `status='published'`.

---

## Component Build Plan

### Phase 1 — Supabase schema
- Create `biome_telemetry`, `telemetry_snapshot`, `setpoint_commands` tables
- Add RLS: `biome_telemetry` and `telemetry_snapshot` read-only public; `setpoint_commands` service-role only

### Phase 2 — Wyse coordinator service
**File:** `telemetry_coordinator.py` (to be placed on the Wyse, run as systemd service)  
**Dependencies:** `paho-mqtt`, `supabase` Python packages  
**Logic:**
- Connect to Mosquitto at `localhost:1883` (Wyse is the broker)
- Subscribe to `miniBIOTA/biome/+/telemetry` and `miniBIOTA/biome/+/status`
- Maintain in-memory latest state per biome (keyed by biome_id)
- Every 60s: insert rows into `biome_telemetry` for all biomes with fresh data
- Every 15s: build snapshot payload → upsert `telemetry_snapshot` row id=1
- Every 5s: query `setpoint_commands` WHERE `status='pending'` → publish each to MQTT → update `status='published'`

**Coordinator state for snapshot:**
- `coordinator.state`: healthy if script is running (self-reported)
- `upstream.state`: healthy/offline based on internet reachability check (ping 8.8.8.8)
- `setpoint_channel.state`: healthy if any setpoint has been published in the last 5 min
- `nodes[N].state`: healthy/stale/offline based on `last_seen` vs. expected 10s publish interval

**Deployment:** systemd service (`minibiota-telemetry.service`) so it starts on boot and restarts on crash.

### Phase 3 — Website update
**File:** `miniBIOTA_Web/utils/telemetry.py`  
**Change:** Replace `MINIBIOTA_TELEMETRY_SNAPSHOT_PATH` file read with a Supabase query on `telemetry_snapshot` (id=1). Fall back to placeholder payload if row is missing or stale.  
**No route changes** — `/live-monitoring` and `/api/telemetry/overview` stay as-is.

### Phase 4 — App Monitoring tab ✓ COMPLETE (2026-04-25)

**Implemented:** `js/monitoring.js`, `css/dashboard.css` (monitoring section), `main.js` (MQTT IPC), `preload.js` (bridge), `index.html` (tab + page skeleton).

**What was built:**
- MQTT-only (no Supabase fallback yet) — direct connect to `192.168.8.228:1883`
- Connection banner: MQTT connected / disconnected state
- 6 biome sub-tabs, each with 7 sensor fields: atmo temp, atmo humidity, bio temp, bio humidity, liquid temp, pump %, setpoint
- Chip status: healthy (<20s), stale (20–45s), offline (>45s), updated every 5s
- Setpoint controls deferred — display-only for now

**Key gotcha resolved:** Firmware was emitting `nan` (not `null`) for missing sensors — invalid JSON silently dropped by `JSON.parse()`. Fixed in firmware (NaN→null). App expects `null` in payload and shows `—` for those fields.

**Remaining from original Phase 4 spec:**
- Setpoint control per biome (number input + Set button → MQTT publish)
- Supabase fallback when off mB2.4 (reads `telemetry_snapshot`)

---

## Decisions Made

| Decision | Choice | Reason |
|---|---|---|
| Telemetry sampling rate (Supabase) | 1 minute | 10s is too much resolution for history; 1min gives adequate granularity |
| Snapshot refresh rate (website) | 15 seconds | Matches existing website contract `refresh_interval_seconds` |
| Snapshot delivery to website | Supabase (not file path) | Railway can't read a local file from the Windows machine |
| Two-way control path | Direct MQTT from app (primary) + Supabase command queue (fallback/record) | Instant control when on mB2.4; Supabase provides audit trail |
| Wyse as always-on aggregator | Yes | Ensures website has data even when app is closed |
| Public telemetry fields | `bio_temp_c`, `bio_humidity_pct`, `atmo_temp_c`, `atmo_humidity_pct` | Liquid temp and pump % are operator-only |
| Monitoring tab location | New 9th tab ("Monitoring") in Electron app | Needs its own space; fits the operator surface role |

---

## Open Items (resolve before build)

- Confirm Python is available on the Wyse (or choose Node.js for the coordinator script)
- Decide whether `setpoint_commands` should also accept future non-temperature parameters (lighting schedule, OTA trigger, etc.) or stay temperature-only for now
- Data retention policy for `biome_telemetry` — 90-day rolling delete, or keep all and revisit when table grows
