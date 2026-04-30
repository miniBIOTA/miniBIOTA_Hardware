# Hardware Agent Protocol

## Purpose
This protocol gives Codex the working rules for repo-native sessions in `miniBIOTA_Hardware`. `AGENTS.md` is the active entry point. `CLAUDE.md` is retained only as legacy context from the earlier Claude workflow.

## Startup Procedure
1. Run the Hardware startup helper when possible:

```powershell
powershell -ExecutionPolicy Bypass -File "_system/codex_session_start.ps1"
```

2. If working manually, read:
   - `AGENTS.md`
   - this file
   - `M:\miniBIOTA\miniBIOTA_Brain\_system\agent_memory.md`
   - `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md`
3. Load only the firmware project or hardware docs needed for the request.
4. Use live MQTT, OTA, router/Wyse access, or Supabase only when the task requires current runtime state.
5. Read `CLAUDE.md` only when checking legacy context that has not yet been migrated into Codex-facing docs.

## Planning Before Writing
For medium or large tasks, plan before writing. Name:
- Firmware projects or docs likely to change.
- Brain brief or mirrored docs that may need updates.
- Live systems that may be touched: ESP32, pump, thermostat, MQTT, OTA, router, Wyse, Supabase telemetry.
- Verification expected before closeout.
- Any approval needed.

Tiny documentation edits can proceed after a short statement of intent when write mode allows it.

## Approval Before Live Actions
Always get explicit approval before:
- Modifying firmware that touches pump switching, thermostat logic, setpoint handling, OTA behavior, WiFi connection behavior, MQTT topics, or telemetry serialization.
- Running USB upload or OTA upload.
- Publishing MQTT setpoints or commands.
- Changing Opal router, Wyse, Mosquitto, or systemd service configuration.
- Creating or changing Supabase telemetry tables, snapshots, or command records.
- Any physical-world action that could affect the living biosphere.

## Firmware Rules
- One PlatformIO project exists per biome folder.
- Preserve local firmware patterns unless the user explicitly scopes a refactor.
- Keep NaN values out of telemetry JSON. Missing sensor values must serialize as JSON `null`.
- MQTT reconnect and WiFi handling must stay non-blocking enough for telemetry and OTA handling.
- Sensor node firmware owns local thermostat/pump behavior. Treat control changes as live-biosphere changes.
- Biome folder numbers match Supabase biome IDs, but always verify against the biome map before editing topics or hostnames.

## Control Network Rules
- The biome network SSID is `mB2.4`.
- Mosquitto runs on the Dell Wyse 3040 at `192.168.8.228:1883`.
- ESP32 nodes publish under `miniBIOTA/biome/<id>/`.
- Sensor telemetry publishes every 10 seconds where sensors exist.
- App Monitoring currently connects directly to MQTT for live operator readings.
- Wyse coordinator, Supabase telemetry tables, and website integration remain planned phases unless current docs say otherwise.

## Documentation Rules
- Source docs live in this repo under `docs/`.
- Brain mirrors under `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\docs\` are read-only copies.
- Update `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_brief.md` when system state, priorities, milestones, risks, or cross-domain dependencies change.
- Do not push raw firmware details into the Brain brief; keep those in hardware docs.

## Git Rules
- Preserve user edits. Never revert changes you did not make unless explicitly asked.
- Keep PlatformIO build outputs, caches, env files, editor state, and logs out of git.
- Before commit, run `git status --short` and inspect the changed file list.
- Use concise commit messages describing the hardware/protocol change.

## Verification
For documentation-only work:
- Read every new or changed document end to end.
- Run `git diff --name-only`.
- Confirm no firmware or live-control behavior changed.

For firmware work:
- Run `pio run --project-dir "<affected biome folder>"` when PlatformIO is available.
- Use upload/OTA only after explicit approval.
- Prefer read-only MQTT subscriptions for telemetry checks.
- Report skipped hardware checks honestly, especially when the device, network, or approval is unavailable.

## Session Closeout
Before final response:
- List touched surfaces.
- Read changed docs or verify changed firmware.
- Check `git status --short`.
- Confirm whether firmware changed.
- Confirm whether live controls, MQTT, OTA, schema, or physical hardware were touched.
- Update Brain or repo docs if durable operating knowledge changed.
- Report unresolved questions.

Use this report shape:

```markdown
Changed files:
- path

Verification:
- check performed

Not changed:
- firmware/live controls/MQTT/schema, unless explicitly changed

Unresolved questions:
- None
```
