# miniBIOTA Hardware - Legacy Claude Context

> Legacy note: miniBIOTA_Hardware now uses Codex as the primary operating interface. This file is retained for historical Claude context only; active Codex rules live in `AGENTS.md` and `docs/agent_protocol.md`.

## What This Repo Is

ESP32 firmware for per-biome sensor nodes in the miniBIOTA closed biosphere. One PlatformIO project per biome, Arduino framework.

## Project Structure

| Folder | Biome | Supabase biome_id |
|---|---|---|
| `1. Freshwater Lake Biome/` | Freshwater Lake | 1 |
| `2. Lakeshore Biome/` | Lakeshore | 2 |
| `3. Lowland Meadow Biome/` | Lowland Meadow | 3 |
| `4. Mangrove Forest Biome/` | Mangrove Forest | 4 |
| `5. Marine Shore Biome/` | Marine Shore | 5 |
| `6. Seagrass Meadow Biome/` | Seagrass Meadow | 6 |

## Platform

- **Module:** ESP-WROOM-32 (ESP32-DevKitC), all 6 nodes
- **Carrier board:** ESP32 Breakout Board with 3.5mm screw terminal GPIO expansion (0.9"/1.0" form factor)
- **Framework:** Arduino via PlatformIO
- **Sensors:** SHT31 (temperature + humidity, I2C) — deployed on biomes 2–5; biome 1 pending hardware
- **Network:** Opal GL-SFT1200 micro-router (2.4 GHz biome network `mB2.4`), upstream 5 GHz
- **MQTT broker:** Mosquitto on Dell Wyse 3040 thin client at `192.168.8.228:1883`
- **Each ESP32 owns:** local thermostat hysteresis, 12 V pump switching, sensor publishing

## How the Control System Works

The Dell Wyse publishes target temperature setpoints via MQTT. Each ESP32 subscribes, owns local PID/hysteresis logic, and publishes telemetry back. The system stays operational if upstream internet fails — control is local.

## Architecture Docs

Detailed system documentation lives in `docs/` within this repo:

| File | Contents |
|---|---|
| `docs/physical_architecture.md` | Structural support, atmosphere mounting, ports, bulkheads, modular layout |
| `docs/climate_and_rain_system.md` | Cooling loop, condensation, cloud reservoirs, rain mechanism |
| `docs/control_network.md` | Opal router, ESP32 nodes, MQTT, sensors, distributed control |
| `docs/hydrological_architecture.md` | Freshwater/marine hydrology, air volume topology, isolation |
| `docs/telemetry_pipeline_plan.md` | Wyse coordinator, Supabase tables, App Monitoring, website integration |
| `docs/control_system_setup.md` | Setup and troubleshooting guide |

These are mirrored read-only into `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\docs\` by `sync_docs.ps1` at Brain session start.

## Strategy Agent Relationship

This repo reports to the **Strategy Agent** at `M:\miniBIOTA\miniBIOTA_Brain`.

The Strategy Agent holds the strategic brief at `6. Engineering & Hardware\engineering_brief.md`. The brief is the only hardware content the Strategy Agent reads by default — it covers system state, priorities, milestones, risks, and cross-domain dependencies. Full architecture docs stay here.

### Brief Update Protocol
At the end of any hardware session, update the brief if any of these changed:
- System or biome state (what's healthy, offline, degraded)
- Active priorities or what's next in the work queue
- Milestones completed
- Risks or blockers (especially anything affecting ecology, content, or operations)
- Cross-domain dependencies (timing of rewires, downtime, naming changes)
- Standardized system names

Write to: `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md`

Do not push: firmware architecture, PlatformIO config, MQTT protocol details, wiring specifics, or setup/troubleshooting guides — those belong in `docs/` here.

## Cross-References

For strategy and operational context, read:
- `M:\miniBIOTA\miniBIOTA_Brain\_system\agent_memory.md`
- `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md`

## Write Policy

Follow the cautious write model from Brain (`agent_memory.md`). Confirm writes with Josue before modifying firmware that touches pump switching or thermostat logic — those affect live ecology.
