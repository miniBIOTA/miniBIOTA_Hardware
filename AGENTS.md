# miniBIOTA Hardware - Codex Agent Entry Point

## What This Repo Is
`miniBIOTA_Hardware` is the firmware, control-network, and hardware operations repo for the miniBIOTA closed biosphere. It contains one PlatformIO/Arduino ESP32 project per biome, repo-local durable memory, repo-local task playbooks, exact hardware references, deployment helpers, and telemetry coordinator code.

Codex is the primary operating interface for this repo. Legacy Claude context has been archived at `archive/legacy/CLAUDE.md` for historical investigation only. Active operating rules belong in `AGENTS.md`, `memory/`, `0. Hardware Systems/`, `skills/`, `skills/*/reference/`, Company Hardware reports, the Brain archive lookup, or Supabase when the record is structured.

## Architecture

| Surface | Purpose |
|---|---|
| `AGENTS.md` | Hard operating rules, safety rules, and routing |
| `memory/` | Compressed durable Hardware Agent knowledge |
| `0. Hardware Systems/` | Six canonical system data sheets and cross-biome hardware architecture |
| `skills/` | Repo-local task playbooks, not globally installed Codex skills |
| `skills/*/reference/` | Exact supporting references for playbooks that need setup, telemetry, deployment, protocol, or legacy architecture detail |
| `1. Freshwater Lake Biome/` through `6. Seagrass Meadow Biome/` | Existing PlatformIO firmware projects |
| `services/` | Host-side telemetry coordinator code and tests |
| `deploy/` | Deployment examples for Wyse/systemd services |
| `_system/` | PowerShell session helpers |
| Supabase / App Planner | Structured telemetry plus live Hardware project/task records |
| Company Hardware reports | Manager-facing current state, priorities, risks, and cross-domain coordination |
| Brain archive lookup | Protocol/archive fallback while Brain-to-Company retirement is in progress |

There is no active `docs/` mirror pattern for Hardware. Detailed source material now lives in biome folders, `0. Hardware Systems/`, memory, local playbooks, and skill reference files.

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
- Use MCP/read-only awareness and Company/domain-owned helpers. Brain tool code is historical/recovery context only for normal workflows.

## Startup Sequence
For a full Codex bootstrap, run:

```powershell
powershell -ExecutionPolicy Bypass -File "_system/codex_session_start.ps1"
```

If working manually:

1. Read `AGENTS.md`.
2. Read `memory/00-index.md`.
3. Read `M:\miniBIOTA\miniBIOTA_Company\company_overview.md` and `M:\miniBIOTA\miniBIOTA_Company\company_brief.md` when cross-domain operating context matters.
4. Read `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md` when current Hardware reporting context matters.
5. Read `M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md` only as transition/archive context while Brain retirement is in progress.
6. Load only the memory files, `0. Hardware Systems/` data sheets, local playbooks, skill reference files, firmware project, service code, or deployment reference needed for the task.

## Routing

- For durable identity, system architecture summaries, control-network state, firmware map, telemetry flow, safety rules, cross-agent relationships, and recurring decisions, use `memory/`.
- For detailed cross-biome system architecture, use `0. Hardware Systems/`.
- For repeatable actions, use repo-local playbooks in `skills/`.
- For session closeout, use `skills/hardware-session-closeout/SKILL.md`.
- For exact setup procedures, topic maps, telemetry plans, deployment detail, or older supporting architecture context, use the relevant playbook's `reference/` folder.
- For deployed firmware behavior, read the affected biome project and `platformio.ini`.
- For telemetry coordinator behavior, read `services/` and `deploy/`.
- For current structured records, use Supabase/App Planner when the task requires live/queryable state.
- Archived legacy Claude context is historical only and does not override Codex-facing docs.

## Source Of Truth
Use this hierarchy when sources disagree:

1. User direction in the current session.
2. Local `AGENTS.md` for hard Hardware Agent operating rules.
3. Firmware source, `platformio.ini`, service code, and deployment files for implemented behavior.
4. Biome `biome_hardware.md` files for per-biome installed hardware.
5. `0. Hardware Systems/` for canonical cross-biome system data sheets and hardware architecture.
6. `memory/` for compressed durable knowledge.
7. Local `skills/` playbooks for repeatable task workflows.
8. Skill `reference/` files for supporting setup procedures, deployment detail, and legacy architecture context.
9. Company `domains/hardware/hardware_brief.md` and `domains/hardware/hardware_overview.md` for manager-facing current state and cross-domain coordination.
10. Brain `6. miniBIOTA_Hardware/hardware_brief.md` for transition/archive state while Brain retirement is in progress.
11. Supabase for structured/queryable records and telemetry schema truth.
12. `archive/legacy/CLAUDE.md` only for historical investigation; it is not active source of truth.

Chat history and private model memory are never source of truth. Durable project memory belongs in Markdown in this repo, in Company Hardware reports or the Brain archive lookup when manager-facing state changes, or in Supabase when it is structured data.

## Biome Project Map
| Folder | Biome | Supabase biome_id | Notes |
|---|---|---:|---|
| `1. Freshwater Lake Biome/` | Freshwater Lake | 1 | No sensors yet; offline expected |
| `2. Lakeshore Biome/` | Lakeshore | 2 | Sensor node; atmo SHT31 currently shows Sensor Err |
| `3. Lowland Meadow Biome/` | Lowland Meadow | 3 | Sensor node; atmo SHT31 shows Sensor Err over unstable data |
| `4. Mangrove Forest Biome/` | Mangrove Forest | 4 | Sensor node; bio SHT31 appears water damaged and biome screen is off |
| `5. Marine Shore Biome/` | Marine Shore | 5 | Sensor node; currently working, with humidity display artifact |
| `6. Seagrass Meadow Biome/` | Seagrass Meadow | 6 | Wave/tide stepper node |

## Safety Rules
- Firmware can affect live ecology. Confirm before modifying pump switching, thermostat logic, setpoint handling, OTA behavior, MQTT control topics, telemetry serialization, WiFi/MQTT connection behavior, or anything that can change live biome conditions.
- Do not flash firmware, publish MQTT setpoints, alter router/Wyse configuration, or change Supabase telemetry schema without explicit user approval.
- Prefer documentation-only changes unless the user explicitly scopes firmware, deployment, schema, or live control-system work.
- Do not create dummy database, telemetry, or MQTT writes to inspect behavior.
- Read-only MQTT subscriptions, service dry-runs, and local tests are allowed when they do not publish commands or alter live state.

## Planner / Project Management
- Hardware work is tracked in the App Planner through Supabase `work_projects` and `tasks`.
- Current Hardware projects live under the Engineering domain with `domain_label = Engineering & Hardware` and `owner_agent = Hardware Agent`.
- At the start of planning-heavy Hardware sessions, read current Planner projects/tasks when choosing next work or checking blockers.
- At closeout, if completed work maps to a Planner task, ask whether to mark that task done unless the user explicitly asked for that live task update.
- Creating/editing Planner projects or tasks, changing status, marking done, archiving, or adding subtasks are live Supabase writes and require explicit user approval.

## Current Hardware Watchouts
- All 6 biome nodes have live firmware; biomes 1-5 were USB-flashed on 2026-04-25 and OTA works going forward.
- Biomes 2-5 have sensor wiring/connection-quality risks and some water-damaged SHT31 modules; firmware is expected to emit valid JSON `null`, not `nan`, for missing readings.
- Biome 1 has no sensors installed and may appear offline.
- Biome 6 is wave-motor-only and not part of the sensor telemetry set yet.
- Biomes 2-5 need a sensor/controller rewire; connector standard remains open. XT30 for power and JST-XH 2.54mm for signal are candidates, not settled requirements.
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

## Company Relationship
This repo reports active operating state to Company through:

`M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_overview.md`
`M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`

Brain transition/archive fallback:

`M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`

Update or flag the Company Hardware reports at session end when system state, active priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change. Keep the Brain archive lookup aligned only while Brain retirement is in progress. Keep implementation details, setup guides, and exact hardware references in this repo, especially in biome folders and `0. Hardware Systems/`.

Brain no longer mirrors Hardware docs. Company and Brain should route deeper Hardware work to this repo's `AGENTS.md`, biome folders, `0. Hardware Systems/`, `memory/`, `skills/`, and `skills/*/reference/`.

## Write Policy
Respect `MINIBIOTA_WRITE_MODE` from Company/Brain when available:

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

If local source files changed in a way Company needs, update or flag the Company Hardware reports before closing unless the user explicitly defers it. Keep the Brain archive lookup and Brain exports aligned only when Brain source files change.
