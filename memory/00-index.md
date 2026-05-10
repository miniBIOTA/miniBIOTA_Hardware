---
id: hardware_memory_index
title: Hardware Memory Index
domain: engineering_and_hardware
last_updated: 2026-05-09
tags: [memory, routing, hardware-agent]
---
# Hardware Memory Index

This folder is the compressed durable memory layer for the miniBIOTA Hardware Agent. It does not replace `AGENTS.md`, firmware source, service code, Supabase, system data sheets under `0. Hardware Systems/`, or exact references under `skills/*/reference/`. It gives Codex a lighter route into the right context for each task.

## Read Order

For every Hardware session:

1. Read `AGENTS.md`.
2. Read this index.
3. Read only the memory files needed for the task.
4. If the task matches a local playbook, read the relevant `skills/*/SKILL.md`.
5. Read `0. Hardware Systems/` files when the task concerns Climate, Rain, Lighting, Wave & Tide, Control System, or Enclosure architecture.
6. Read skill reference files only when the task requires setup procedures, exact topic maps, deployment commands, or telemetry contracts.
7. Read affected firmware/service files before changing implemented behavior.
8. Use Supabase/App Planner when current structured telemetry, project, or task records matter.

## Memory Files

| File | Use When |
|---|---|
| `memory/01-agent-purpose.md` | Understanding the Hardware Agent's role, boundaries, and relationship to Josue, Company, and Brain |
| `memory/02-system-architecture.md` | Orienting around physical, hydrological, climate, rain, and enclosure architecture |
| `memory/03-control-network.md` | Working with Opal, Wyse, Mosquitto, ESP32 nodes, MQTT, and sensor topology |
| `memory/04-firmware-and-biome-map.md` | Choosing the correct PlatformIO project, biome ID, firmware status, and build/upload path |
| `memory/05-database-access.md` | Hardware database access boundaries, owned/read/write tables, and Company reporting expectations |
| `memory/05-telemetry-and-data-flow.md` | Working with App Monitoring, Wyse coordinator, Supabase telemetry, website snapshots, or MQTT payloads |
| `memory/06-hardware-safety-rules.md` | Checking approval gates and live-biosphere safety rules |
| `memory/07-cross-agent-relationships.md` | Deciding what belongs in Hardware, Company, Brain, App, Web, Content, Research, or Supabase |
| `memory/08-recurring-decisions.md` | Checking durable decisions that should not be rediscovered each session |
| `memory/inbox.md` | Temporary holding area for candidate durable memory before it is promoted to a named memory file |

## Local Skill Playbooks

These are repo-local task playbooks, not globally installed Codex skills. Load them when the user's request matches the trigger phrases.

| Playbook | Use When |
|---|---|
| `skills/firmware-build-and-verify/SKILL.md` | Building, reviewing, or changing ESP32 firmware for a biome |
| `skills/control-network-setup/SKILL.md` | Setting up or troubleshooting Opal, Wyse, Mosquitto, MQTT topics, node leases, or OTA routing |
| `skills/telemetry-coordinator/SKILL.md` | Working on the Wyse telemetry coordinator, website snapshot contract, Supabase telemetry plan, or coordinator tests |
| `skills/hardware-architecture-reference/SKILL.md` | Answering physical, hydrological, climate, rain, enclosure, or system-boundary questions |
| `skills/update-hardware-memory/SKILL.md` | Promoting durable Hardware decisions or repeated instructions into memory safely |
| `skills/hardware-session-closeout/SKILL.md` | Closing Hardware sessions with verification, Company report checks, Brain transition checks, and live-system non-change confirmation |

## System Data Sheets

| Folder | Use When |
|---|---|
| `0. Hardware Systems/README.md` | Routing among the six canonical public systems |
| `0. Hardware Systems/1. Climate System/` | Chiller, coolant loop, pumps, heat exchangers, and climate delivery |
| `0. Hardware Systems/2. Rain System/` | Cloud reservoirs, rain manifolds, condensate collection, and rainfall distribution |
| `0. Hardware Systems/3. Lighting System/` | Photoperiod, spectrum, fixtures, and lighting control |
| `0. Hardware Systems/4. Wave & Tide System/` | Stepper motor, swash mechanics, encoder, and tide/wave simulation |
| `0. Hardware Systems/5. Control System/` | ESP32 nodes, sensors, MQTT, Opal, Wyse, telemetry, and local control model |
| `0. Hardware Systems/6. Enclosure/` | Tanks, cabinets, ports, bulkheads, sealing, and closure boundary |

## Source Boundaries

- `memory/` summarizes durable knowledge. It should stay concise.
- `0. Hardware Systems/` contains canonical cross-biome system data sheets and hardware architecture.
- `skills/` contains the active workflow layer. Use playbooks for repeatable actions instead of old workflow docs.
- `skills/*/reference/` holds exact setup, telemetry, firmware, deployment, and legacy architecture references for playbooks that need them.
- Firmware source and `platformio.ini` remain the truth for deployed code behavior.
- `services/` and `deploy/` remain the truth for host-side telemetry coordinator behavior.
- Supabase remains canonical for structured telemetry, task, project, and domain records when those tables exist.
- Company `domains/hardware/hardware_brief.md` and `domains/hardware/hardware_overview.md` are the active manager-facing current-state reports; Brain `6. miniBIOTA_Hardware/hardware_brief.md` remains transition/archive context while Brain retirement is in progress.
- `archive/legacy/CLAUDE.md` is historical reference only, not active startup context.
- The old Hardware `docs/` mirror pattern is retired.
