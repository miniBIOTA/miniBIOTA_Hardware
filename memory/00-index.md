---
id: hardware_memory_index
title: Hardware Memory Index
domain: engineering_and_hardware
last_updated: 2026-05-05
tags: [memory, routing, hardware-agent]
---
# Hardware Memory Index

This folder is the compressed durable memory layer for the miniBIOTA Hardware Agent. It does not replace `AGENTS.md`, firmware source, service code, Supabase, or exact references under `skills/*/reference/`. It gives Codex a lighter route into the right context for each task.

## Read Order

For every Hardware session:

1. Read `AGENTS.md`.
2. Read this index.
3. Read only the memory files needed for the task.
4. If the task matches a local playbook, read the relevant `skills/*/SKILL.md`.
5. Read skill reference files only when the task requires setup detail, exact topic maps, architecture reference, deployment commands, or telemetry contracts.
6. Read affected firmware/service files before changing implemented behavior.
7. Use Supabase through the Brain tool layer when current structured records matter.

## Memory Files

| File | Use When |
|---|---|
| `memory/01-agent-purpose.md` | Understanding the Hardware Agent's role, boundaries, and relationship to Josue and Brain |
| `memory/02-system-architecture.md` | Orienting around physical, hydrological, climate, rain, and enclosure architecture |
| `memory/03-control-network.md` | Working with Opal, Wyse, Mosquitto, ESP32 nodes, MQTT, and sensor topology |
| `memory/04-firmware-and-biome-map.md` | Choosing the correct PlatformIO project, biome ID, firmware status, and build/upload path |
| `memory/05-database-access.md` | Hardware database access boundaries, owned/read/write tables, and Brain reporting expectations |
| `memory/05-telemetry-and-data-flow.md` | Working with App Monitoring, Wyse coordinator, Supabase telemetry, website snapshots, or MQTT payloads |
| `memory/06-hardware-safety-rules.md` | Checking approval gates and live-biosphere safety rules |
| `memory/07-cross-agent-relationships.md` | Deciding what belongs in Hardware, Brain, App, Web, Content, Research, or Supabase |
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

## Source Boundaries

- `memory/` summarizes durable knowledge. It should stay concise.
- `skills/` contains the active workflow layer. Use playbooks for repeatable actions instead of old workflow docs.
- `skills/*/reference/` holds exact setup, architecture, telemetry, and firmware references for playbooks that need them.
- Firmware source and `platformio.ini` remain the truth for deployed code behavior.
- `services/` and `deploy/` remain the truth for host-side telemetry coordinator behavior.
- Supabase remains canonical for structured telemetry, task, and domain records when those tables exist.
- Brain `6. miniBIOTA_Hardware/hardware_brief.md` remains the strategy-level current-state brief.
- `archive/legacy/CLAUDE.md` is historical reference only, not active startup context.
- The old Hardware `docs/` mirror pattern is retired.
