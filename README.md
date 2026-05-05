# miniBIOTA Hardware

Firmware, control-network, telemetry, and hardware operations repo for the miniBIOTA closed biosphere.

## Start A Codex Session

```powershell
powershell -ExecutionPolicy Bypass -File "_system/codex_session_start.ps1"
```

Then read the files listed by the helper, especially `AGENTS.md`, `memory/00-index.md`, Brain `agent_memory.md`, the Hardware engineering brief, and the relevant memory/playbook/reference files or biome project.

## Repository Shape

| Path | Purpose |
|---|---|
| `AGENTS.md` | Codex entry point and repo operating rules |
| `memory/` | Compressed durable Hardware Agent memory |
| `skills/` | Repo-local task playbooks |
| `skills/*/reference/` | Exact setup, architecture, telemetry, and firmware references |
| `CLAUDE.md` | Legacy Claude context, retained for reference only |
| `1. Freshwater Lake Biome/` | PlatformIO project for biome 1 |
| `2. Lakeshore Biome/` | PlatformIO project for biome 2 |
| `3. Lowland Meadow Biome/` | PlatformIO project for biome 3 |
| `4. Mangrove Forest Biome/` | PlatformIO project for biome 4 |
| `5. Marine Shore Biome/` | PlatformIO project for biome 5 |
| `6. Seagrass Meadow Biome/` | PlatformIO project for biome 6 |
| `services/` | Wyse telemetry coordinator code and tests |
| `deploy/` | Deployment examples |
| `_system/` | Codex session helpers |

The old `docs/` mirror pattern is retired. Hardware detail now routes through `memory/`, `skills/`, and `skills/*/reference/`.

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

MQTT publishing, Supabase schema changes, Wyse deployment, and command processing remain separate approval-gated actions.

## Brain Link

This domain reports to the Strategy Agent through:

`M:\miniBIOTA\miniBIOTA_Brain\6. miniBIOTA_Hardware\hardware_brief.md`

Update that brief when system state, active priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change.

Brain no longer mirrors Hardware docs. Use this repo's `AGENTS.md`, `memory/`, `skills/`, and `skills/*/reference/` for detailed Hardware context.

## GitHub

Remote:

`https://github.com/miniBIOTA/miniBIOTA_Hardware.git`

Track firmware source, memory, playbooks, reference files, helper scripts, services, deployment examples, and migrations/specs. Keep PlatformIO build outputs, caches, env files, logs, and local editor state out of git.
