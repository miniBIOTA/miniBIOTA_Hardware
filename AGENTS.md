# miniBIOTA Hardware - Codex Agent Entry Point

## What This Repo Is
`miniBIOTA_Hardware` is the firmware, control-network, and hardware operations repo for the miniBIOTA closed biosphere. It contains one PlatformIO/Arduino ESP32 project per biome, repo-local durable memory, repo-local task playbooks, exact hardware references, deployment helpers, and telemetry coordinator code.

Codex is the primary operating interface for this repo. `CLAUDE.md` remains legacy context only; active operating rules belong in `AGENTS.md`, `memory/`, `skills/`, `skills/*/reference/`, Brain `engineering_brief.md`, or Supabase when the record is structured.

## Architecture

| Surface | Purpose |
|---|---|
| `AGENTS.md` | Hard operating rules, safety rules, and routing |
| `memory/` | Compressed durable Hardware Agent knowledge |
| `skills/` | Repo-local task playbooks, not globally installed Codex skills |
| `skills/*/reference/` | Exact supporting references for playbooks that need setup, architecture, or protocol detail |
| `1. Freshwater Lake Biome/` through `6. Seagrass Meadow Biome/` | Existing PlatformIO firmware projects |
| `services/` | Host-side telemetry coordinator code and tests |
| `deploy/` | Deployment examples for Wyse/systemd services |
| `_system/` | PowerShell session helpers |
| Supabase | Structured telemetry, task, and domain records when implemented |
| Brain engineering brief | Strategy-level current state and cross-domain coordination |

There is no active `docs/` mirror pattern for Hardware. Detailed source material now lives in memory, local playbooks, and skill reference files.

## Tech Stack
- PlatformIO projects using the Arduino framework.
- ESP-WROOM-32 / ESP32-DevKitC nodes.
- SHT31 temperature/humidity sensors on biomes 2-5.
- DS18B20 liquid temperature probes where installed.
- MQTT over the local `mB2.4` biome network.
- Mosquitto broker on Dell Wyse 3040 at `192.168.8.228:1883`.
- Opal GL-SFT1200 router for the isolated biome network.
- OTA firmware upload after each node has been USB-flashed once.
- Python Wyse telemetry coordinator under `services/`.
- Brain tool layer at `M:\miniBIOTA\miniBIOTA_Brain\_system\minibiota_tools.py`.

## Startup Sequence
For a full Codex bootstrap, run:

```powershell
powershell -ExecutionPolicy Bypass -File "_system/codex_session_start.ps1"
```

If working manually:

1. Read `AGENTS.md`.
2. Read `memory/00-index.md`.
3. Read `M:\miniBIOTA\miniBIOTA_Brain\_system\agent_memory.md`.
4. Read `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md`.
5. Load only the memory files, local playbooks, skill reference files, firmware project, service code, or deployment reference needed for the task.
6. Read `CLAUDE.md` only when checking legacy context that has not yet been migrated into Codex-facing docs.

## Routing

- For durable identity, system architecture, control-network state, firmware map, telemetry flow, safety rules, cross-agent relationships, and recurring decisions, use `memory/`.
- For repeatable actions, use repo-local playbooks in `skills/`.
- For exact setup procedures, topic maps, physical architecture, telemetry plans, or deployment detail, use the relevant playbook's `reference/` folder.
- For deployed firmware behavior, read the affected biome project and `platformio.ini`.
- For telemetry coordinator behavior, read `services/` and `deploy/`.
- For current structured records, use Supabase through the Brain tool layer only when the task requires live/queryable state.
- For legacy details not yet migrated, use `CLAUDE.md` sparingly and treat it as lower-priority legacy context.

## Source Of Truth
Use this hierarchy when sources disagree:

1. User direction in the current session.
2. Local `AGENTS.md` for hard Hardware Agent operating rules.
3. Firmware source, `platformio.ini`, service code, and deployment files for implemented behavior.
4. `memory/` for compressed durable knowledge.
5. Local `skills/` playbooks for repeatable task workflows.
6. Skill `reference/` files for supporting setup, architecture, and technical detail.
7. Brain `6. Engineering & Hardware/engineering_brief.md` for strategy-level current state.
8. Supabase for structured/queryable records and telemetry schema truth.
9. `CLAUDE.md` only as legacy context when a needed rule or detail has not yet been migrated.

Chat history and private model memory are never source of truth. Durable project memory belongs in Markdown in this repo, in the Brain engineering brief, or in Supabase when it is structured data.

## Biome Project Map
| Folder | Biome | Supabase biome_id | Notes |
|---|---|---:|---|
| `1. Freshwater Lake Biome/` | Freshwater Lake | 1 | No sensors yet; offline expected |
| `2. Lakeshore Biome/` | Lakeshore | 2 | Sensor node; known atmo SHT31 wiring fault |
| `3. Lowland Meadow Biome/` | Lowland Meadow | 3 | Sensor node; known atmo SHT31 intermittent wiring fault |
| `4. Mangrove Forest Biome/` | Mangrove Forest | 4 | Sensor node; known bio SHT31 wiring fault |
| `5. Marine Shore Biome/` | Marine Shore | 5 | Sensor node; known bio SHT31 wiring fault |
| `6. Seagrass Meadow Biome/` | Seagrass Meadow | 6 | Wave/tide stepper node |

## Safety Rules
- Firmware can affect live ecology. Confirm before modifying pump switching, thermostat logic, setpoint handling, OTA behavior, MQTT control topics, telemetry serialization, WiFi/MQTT connection behavior, or anything that can change live biome conditions.
- Do not flash firmware, publish MQTT setpoints, alter router/Wyse configuration, or change Supabase telemetry schema without explicit user approval.
- Prefer documentation-only changes unless the user explicitly scopes firmware, deployment, schema, or live control-system work.
- Do not create dummy database, telemetry, or MQTT writes to inspect behavior.
- Read-only MQTT subscriptions, service dry-runs, and local tests are allowed when they do not publish commands or alter live state.

## Current Hardware Watchouts
- All 6 biome nodes have live firmware; biomes 1-5 were USB-flashed on 2026-04-25 and OTA works going forward.
- Biomes 2-5 have wiring faults causing some SHT31 readings to be `null`; firmware is expected to emit valid JSON `null`, not `nan`.
- Biome 1 has no sensors installed and may appear offline.
- Biome 6 is wave-motor-only and not part of the sensor telemetry set yet.
- The planned rewire for biomes 2-5 uses XT30 for power and JST-XH 2.54mm for signal.
- Firmware previously fixed three important bugs: WiFi hang timeout, non-blocking MQTT reconnect, and NaN-to-null telemetry serialization.
- `services/telemetry_coordinator.py` is read-only by design: it subscribes to MQTT and writes snapshots, but does not publish setpoints, pump commands, actuator commands, or firmware updates.

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

Update that brief at session end when system state, active priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change. Keep implementation details, setup guides, and exact hardware references in this repo.

Brain no longer mirrors Hardware docs. Brain should route deeper Hardware work to this repo's `AGENTS.md`, `memory/`, `skills/`, and `skills/*/reference/`.

## Write Policy
Respect `MINIBIOTA_WRITE_MODE` from Brain when available:

| Mode | Behavior |
|---|---|
| `read-only` | No writes anywhere |
| `confirm-before-write` | Confirm with the user before writes |
| `safe-write` | Writes may proceed after stating what will change |

For this repo, tell the user what files you intend to change before editing. Preserve user changes and keep edits scoped to the active request.

Always get explicit approval before irreversible deletion outside an explicit deletion scope, firmware upload, live MQTT command, router/Wyse configuration change, Supabase schema/table change, or any physical-world action affecting the living biosphere.

## Verification
For documentation-only sessions:
- Read every new or changed doc end to end.
- Run `git diff --name-only` or equivalent.
- Confirm no firmware, schema, MQTT, OTA, or live control behavior changed.

For firmware sessions:
- Run `pio run` for the affected biome project when practical.
- Run upload/OTA only after explicit approval.
- Verify MQTT/telemetry behavior with read-only subscriptions or app observation when relevant.
- Report any hardware, WiFi, MQTT, or live-biosphere checks that were skipped and why.

For telemetry coordinator sessions:
- Run focused tests when practical, usually `python -m unittest discover services/tests`.
- Use dry-run or local snapshot output for contract verification when possible.
- Treat MQTT publishing, Supabase schema changes, and service deployment as separate approval-gated actions.

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

If local source files changed in a way the Strategy Agent needs, update the Brain engineering brief before closing unless the user explicitly defers it. Brain exports should be rebuilt after Brain source files change unless explicitly deferred.
