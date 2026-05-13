# miniBIOTA Hardware

Firmware, control-network, telemetry, and hardware operations repo for the miniBIOTA closed biosphere.

## Start A Codex Session

```powershell
powershell -ExecutionPolicy Bypass -File "_system/codex_session_start.ps1"
```

Then read the files listed by the helper, especially `AGENTS.md`, `memory/00-index.md`, the Company Hardware brief when current reporting context matters, the Brain archive lookup only when needed, and the relevant biome, system, memory, playbook, or reference files.

## Repository Shape

| Path | Purpose |
|---|---|
| `AGENTS.md` | Codex entry point and repo operating rules |
| `memory/` | Compressed durable Hardware Agent memory |
| `0. Hardware Systems/` | Six canonical hardware systems and cross-biome architecture/data sheets |
| `skills/` | Repo-local task playbooks |
| `skills/*/reference/` | Exact setup, telemetry, firmware, deployment, and legacy architecture references |
| `archive/legacy/CLAUDE.md` | Historical Claude context, not active operating guidance |
| `1. Freshwater Lake Biome/` | PlatformIO project for biome 1 |
| `2. Lakeshore Biome/` | PlatformIO project for biome 2 |
| `3. Lowland Meadow Biome/` | PlatformIO project for biome 3 |
| `4. Mangrove Forest Biome/` | PlatformIO project for biome 4 |
| `5. Marine Shore Biome/` | PlatformIO project for biome 5 |
| `6. Seagrass Meadow Biome/` | PlatformIO project for biome 6 |
| `services/` | Wyse telemetry coordinator code and tests |
| `deploy/` | Deployment examples |
| `_system/` | Codex session helpers |

The old `docs/` mirror pattern is retired. Hardware detail now routes through biome folders, `0. Hardware Systems/`, `memory/`, `skills/`, and `skills/*/reference/`.

## System Documentation

The canonical system-level architecture lives in `0. Hardware Systems/`:

| Folder | System |
|---|---|
| `0. Hardware Systems/1. Climate System/` | Climate System |
| `0. Hardware Systems/2. Rain System/` | Rain System |
| `0. Hardware Systems/3. Lighting System/` | Lighting System |
| `0. Hardware Systems/4. Wave & Tide System/` | Wave & Tide System |
| `0. Hardware Systems/5. Control System/` | Control System |
| `0. Hardware Systems/6. Enclosure/` | Enclosure |

Biome folders remain top-level PlatformIO implementation projects. Use biome folders for exact installed hardware and firmware; use `0. Hardware Systems/` for cross-biome architecture and shared system data sheets.

## Firmware Commands

Build a biome project:

```powershell
pio run --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

USB upload:

```powershell
pio run -e esp32dev -t upload --upload-port COMX --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

OTA upload:

```powershell
pio run -e esp32dev_ota -t upload --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

Do not run upload/OTA commands without explicit approval; firmware can affect live biosphere conditions.

## Telemetry Coordinator

Run focused tests when changing the read-only Wyse coordinator:

```powershell
python -m unittest discover services/tests
```

Dry-run a sample website-compatible snapshot:

```powershell
python services/telemetry_coordinator.py --dry-run
```

Internal history schema for climate/control analysis:

`services/schema/biome_telemetry_schema_2026-05-13.sql`

MQTT publishing, Supabase schema changes, Wyse deployment, and command processing remain separate approval-gated actions.

## Company Link

This domain reports active operating state to Company through:

`M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_overview.md`
`M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`

Brain transition/archive fallback:

`M:\miniBIOTA\miniBIOTA_Company\domains\hardware\hardware_brief.md`

Update or flag the Company Hardware reports when system state, active priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change. Keep the Brain archive lookup aligned only while Brain retirement is in progress.

Brain no longer mirrors Hardware docs. Use this repo's `AGENTS.md`, biome folders, `0. Hardware Systems/`, `memory/`, `skills/`, and `skills/*/reference/` for detailed Hardware context.

## GitHub

Remote:

`https://github.com/miniBIOTA/miniBIOTA_Hardware.git`

Track firmware source, memory, playbooks, reference files, helper scripts, services, deployment examples, and migrations/specs. Keep PlatformIO build outputs, caches, env files, logs, and local editor state out of git.
