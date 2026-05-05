---
name: firmware-build-and-verify
description: Repo-local playbook for reviewing, building, or changing miniBIOTA ESP32 PlatformIO firmware safely.
---
# Firmware Build And Verify

This is a repo-local Hardware Agent playbook. It is not a globally installed Codex skill.

## Trigger Phrases

Use this playbook when Josue says things like:

- "Build biome 4 firmware."
- "Fix this ESP32 code."
- "Check the OTA config."
- "Why is this sensor node offline?"
- "Update the pump logic."
- "Change telemetry JSON."

## Required Memory

- `memory/04-firmware-and-biome-map.md`
- `memory/06-hardware-safety-rules.md`
- `memory/08-recurring-decisions.md`

## Required References

- `skills/firmware-build-and-verify/reference/biome-firmware-notes.md`
- The affected biome folder's `platformio.ini` and `src/main.cpp`

## Workflow

1. Identify the biome folder, biome ID, hostname, and firmware role.
2. Read the affected `platformio.ini` and source files before proposing changes.
3. Check whether the requested change touches an approval-gated surface.
4. If it touches live-control behavior, OTA/upload, WiFi/MQTT behavior, topic names, or telemetry serialization, get explicit approval before editing.
5. Keep changes local to the affected project unless the bug is clearly shared across projects.
6. Preserve valid JSON telemetry. Missing readings must be `null`.
7. Preserve non-blocking WiFi/MQTT/OTA behavior.
8. Build with `pio run --project-dir "<biome folder>"` when practical.
9. Do not upload or OTA without explicit approval.
10. Report firmware projects changed, build result, skipped hardware checks, and live surfaces not touched.

## Expected Output

```markdown
Firmware work:
- Biome:
- Files changed:
- Approval-gated surfaces:
- Build:
- Upload/OTA:
- Live checks:
```

## Write And Approval Rules

- Respect `MINIBIOTA_WRITE_MODE`.
- Ask before firmware changes that can affect live ecology.
- Ask before any upload or OTA command.
- Ask before MQTT publishes, router/Wyse config changes, or Supabase telemetry schema changes.
- Do not create dummy MQTT or telemetry writes.
