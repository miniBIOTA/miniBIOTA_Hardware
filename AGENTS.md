# miniBIOTA Hardware - Codex Agent Entry Point

## What This Repo Is
`miniBIOTA_Hardware` is the firmware and hardware documentation repo for the miniBIOTA closed biosphere. It contains one PlatformIO/Arduino ESP32 project per biome, plus architecture docs for the control network, hydrology, climate/rain system, physical system, and telemetry pipeline.

Codex is the primary operating interface for this repo moving forward. `CLAUDE.md` remains as legacy context only; active operating rules belong in `AGENTS.md`, `docs/agent_protocol.md`, Brain Markdown, or Supabase when the record is structured.

## Tech Stack
- PlatformIO projects using the Arduino framework.
- ESP-WROOM-32 / ESP32-DevKitC nodes.
- SHT31 temperature/humidity sensors on biomes 2-5.
- DS18B20 liquid temperature probes where installed.
- MQTT over the local `mB2.4` biome network.
- Mosquitto broker on Dell Wyse 3040 at `192.168.8.228:1883`.
- Opal GL-SFT1200 router for the isolated biome network.
- OTA firmware upload after each node has been USB-flashed once.
- Brain tool layer at `M:\miniBIOTA\miniBIOTA_Brain\_system\minibiota_tools.py`.

## Startup Sequence
For a full Codex bootstrap, run:

```powershell
powershell -ExecutionPolicy Bypass -File "_system/codex_session_start.ps1"
```

If working manually:

1. Read `AGENTS.md`.
2. Read `docs/agent_protocol.md`.
3. Read `M:\miniBIOTA\miniBIOTA_Brain\_system\agent_memory.md`.
4. Read `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md`.
5. Load only the specific firmware project or hardware doc needed for the task.
6. Read `CLAUDE.md` only when checking legacy context that has not yet been migrated into Codex-facing docs.

## Source Of Truth
Use this hierarchy when sources disagree:

1. User direction in the current session.
2. `AGENTS.md` and `docs/agent_protocol.md` for Hardware Agent operating rules.
3. Brain `engineering_brief.md` for strategy-level current state.
4. Hardware `docs/` for architecture and setup detail.
5. Firmware source and `platformio.ini` files for deployed code behavior.
6. Supabase for structured/queryable records and telemetry schema truth.
7. `CLAUDE.md` only as legacy context.

Chat history and private model memory are never source of truth. Durable project memory belongs in Markdown in this repo/vault, in Brain, or in Supabase when it is structured data.

## Biome Project Map
| Folder | Biome | Supabase biome_id | Notes |
|---|---|---:|---|
| `1. Freshwater Lake Biome/` | Freshwater Lake | 1 | No sensors yet; offline expected |
| `2. Lakeshore Biome/` | Lakeshore | 2 | Sensor node; known atmo SHT31 wiring fault |
| `3. Lowland Meadow Biome/` | Lowland Meadow | 3 | Sensor node; known atmo SHT31 intermittent wiring fault |
| `4. Mangrove Forest Biome/` | Mangrove Forest | 4 | Sensor node; known bio SHT31 wiring fault |
| `5. Marine Shore Biome/` | Marine Shore | 5 | Sensor node; known bio SHT31 wiring fault |
| `6. Seagrass Meadow Biome/` | Seagrass Meadow | 6 | Wave/tide stepper node |

## Architecture Docs
| File | Contents |
|---|---|
| `docs/physical_architecture.md` | Structural support, atmosphere mounting, ports, bulkheads, modular layout |
| `docs/climate_and_rain_system.md` | Cooling loop, condensation, cloud reservoirs, rain mechanism |
| `docs/control_network.md` | Opal router, ESP32 nodes, MQTT, sensors, distributed control |
| `docs/hydrological_architecture.md` | Freshwater/marine hydrology, air volume topology, isolation |
| `docs/telemetry_pipeline_plan.md` | Wyse coordinator, Supabase tables, App Monitoring, website integration |
| `docs/control_system_setup.md` | Setup and troubleshooting guide |
| `docs/agent_protocol.md` | Codex operating protocol for hardware sessions |

Docs are mirrored read-only into `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\docs\` by Brain `sync_docs.ps1`. Edit source docs here, not the Brain mirror.

## Safety Rules
- Firmware can affect live ecology. Confirm before modifying pump switching, thermostat logic, setpoint handling, OTA behavior, MQTT control topics, or anything that can change live biome conditions.
- Do not flash firmware, publish MQTT setpoints, alter router/Wyse configuration, or change Supabase telemetry schema without explicit user approval.
- Prefer documentation-only changes unless the user explicitly scopes firmware or control-system work.
- Do not create dummy database, telemetry, or MQTT writes to inspect behavior.

## Current Hardware Watchouts
- All 6 biome nodes have live firmware; biomes 1-5 were USB-flashed on 2026-04-25 and OTA works going forward.
- Biomes 2-5 have wiring faults causing some SHT31 readings to be `null`; firmware is expected to emit valid JSON `null`, not `nan`.
- Biome 1 has no sensors installed and may appear offline.
- Biome 6 is wave-motor-only and not part of the sensor telemetry set yet.
- The planned rewire for biomes 2-5 uses XT30 for power and JST-XH 2.54mm for signal.
- Firmware previously fixed three important bugs: WiFi hang timeout, non-blocking MQTT reconnect, and NaN-to-null telemetry serialization.

## Run Commands
Use the relevant project folder in commands:

```powershell
pio run --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
pio run -e esp32dev -t upload --upload-port COMX --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
pio run -e esp32dev_ota -t upload --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

USB upload is for first flash or recovery. OTA upload is the normal path after current firmware is installed. Do not run upload commands without explicit approval.

## Brain Relationship
This repo reports to the Strategy Agent through:

`M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md`

Update that brief at session end when system state, active priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change. Keep firmware details and setup guides in this repo.

## Write Policy
Respect `MINIBIOTA_WRITE_MODE` from Brain when available:

| Mode | Behavior |
|---|---|
| `read-only` | No writes anywhere |
| `confirm-before-write` | Confirm with the user before writes |
| `safe-write` | Writes may proceed after stating what will change |

For this repo, tell the user what files you intend to change before editing. Preserve user changes and keep edits scoped to the active request.

## Verification
For documentation-only sessions:
- Read every new or changed doc end to end.
- Run `git diff --name-only` or equivalent.
- Confirm no firmware, schema, MQTT, or live control behavior changed.

For firmware sessions:
- Run `pio run` for the affected biome project when practical.
- Run upload/OTA only after explicit user approval.
- Verify MQTT/telemetry behavior with read-only subscriptions or app observation when relevant.
- Report any hardware, WiFi, MQTT, or live-biosphere checks that were skipped and why.

## Session Closeout Report
Close every session with:

```markdown
Changed files:
- path

Verification:
- command or read-through performed

Not changed:
- firmware/live controls/schema/etc. as relevant

Unresolved questions:
- item or "None"
```

If hardware source docs changed, sync Brain mirrored docs and rebuild Brain exports unless the user explicitly defers it.
