# miniBIOTA Hardware

Firmware and hardware documentation for the miniBIOTA closed biosphere control system.

## Start A Codex Session

```powershell
powershell -ExecutionPolicy Bypass -File "_system/codex_session_start.ps1"
```

Then read the files listed by the helper, especially `AGENTS.md`, `docs/agent_protocol.md`, Brain `agent_memory.md`, the hardware brief, and the relevant biome project or architecture doc.

## Repository Shape

| Path | Purpose |
|---|---|
| `AGENTS.md` | Codex entry point and repo operating rules |
| `docs/agent_protocol.md` | Detailed Codex workflow for hardware sessions |
| `CLAUDE.md` | Legacy Claude context, retained for reference only |
| `1. Freshwater Lake Biome/` | PlatformIO project for biome 1 |
| `2. Lakeshore Biome/` | PlatformIO project for biome 2 |
| `3. Lowland Meadow Biome/` | PlatformIO project for biome 3 |
| `4. Mangrove Forest Biome/` | PlatformIO project for biome 4 |
| `5. Marine Shore Biome/` | PlatformIO project for biome 5 |
| `6. Seagrass Meadow Biome/` | PlatformIO project for biome 6 |
| `docs/` | Hardware architecture, setup, and telemetry docs |
| `_system/` | Codex session helpers |

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

## Brain Link

This domain reports to the Strategy Agent through:

`M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md`

Update that brief when system state, active priorities, milestones, risks, blockers, cross-domain dependencies, or canonical system names change.

## GitHub

Remote:

`https://github.com/miniBIOTA/miniBIOTA_Hardware.git`

Track firmware source, docs, helper scripts, and migrations/specs. Keep PlatformIO build outputs, caches, env files, logs, and local editor state out of git.
