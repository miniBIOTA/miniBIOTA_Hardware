---
id: recurring_hardware_decisions
title: Recurring Decisions
domain: engineering_and_hardware
last_updated: 2026-05-05
tags: [memory, decisions, rules]
---
# Recurring Decisions

These are durable Hardware decisions that should not be rediscovered every session.

## Architecture And Routing

- Hardware uses `AGENTS.md`, `memory/`, `skills/`, and `skills/*/reference/` as the active detailed context.
- The old Hardware `docs/` mirror pattern is retired; Brain should not mirror Hardware docs.
- Brain gets strategy-level summaries in `6. miniBIOTA_Hardware/hardware_brief.md`, not raw setup guides.
- Detailed setup and architecture material belongs in local skill reference files.
- `CLAUDE.md` remains legacy context only.

## Control Model

- ESP32 nodes own local thermostat/pump behavior.
- Higher-level surfaces publish setpoints, not direct pump ON/OFF commands, unless explicitly redesigned and approved.
- Nodes continue regulating from the last known target temperature when the thin client, App, or internet is unavailable.
- The local biome network should continue operating even if building internet fails.

## Firmware Rules

- Missing sensor readings serialize as JSON `null`, never `nan`.
- WiFi connection and MQTT reconnect behavior must not block indefinitely.
- OTA handling must not be starved by reconnect loops or long blocking control code.
- Folder numbers match Supabase biome IDs.
- Biome 1 has no sensors and may appear offline.
- Biome 6 is wave/tide only in current telemetry assumptions.

## Sensors And Wiring

- Deployed sensor nodes currently use SHT31 sensors on biomes 2-5.
- Biomes 2-5 have known SHT31 wiring faults; firmware should tolerate `null` readings until rewire.
- Planned rewire uses XT30 for power and JST-XH 2.54mm for signal.
- Treat any old SHT4x wording as future/legacy unless the affected hardware or firmware has been updated.

## Telemetry

- App Monitoring is the live operator surface over direct MQTT.
- The first Wyse telemetry coordinator implementation is read-only.
- Coordinator history inserts and setpoint command polling remain deferred until explicitly scoped.
- Website telemetry should be public-safe and read-only.
- `telemetry_snapshot` is the singleton website current-state row when Supabase integration is active.

## Safety And Writes

- Uploads, OTA, MQTT publishes, router/Wyse changes, Supabase schema changes, and physical live-system actions require explicit approval.
- Documentation-only sessions must still confirm no firmware, schema, MQTT, OTA, or live control behavior changed.
- Do not create dummy telemetry, database, or MQTT writes to inspect behavior.
