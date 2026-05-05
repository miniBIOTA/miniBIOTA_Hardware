---
id: hardware_safety_rules
title: Hardware Safety Rules
domain: engineering_and_hardware
last_updated: 2026-05-05
tags: [memory, safety, approval, live-control]
---
# Hardware Safety Rules

Hardware work can affect a living biosphere. Treat live control, firmware upload, router/Wyse changes, and telemetry schema writes as approval-gated actions.

## Always Ask First

Get explicit user approval before:

- Running USB firmware uploads.
- Running OTA firmware uploads.
- Publishing MQTT setpoints or commands.
- Changing pump switching, PWM behavior, thermostat logic, hysteresis, or setpoint handling.
- Changing OTA behavior, WiFi connection behavior, MQTT topic names, or telemetry serialization in deployed firmware.
- Changing Opal router configuration, DHCP leases, Wyse system configuration, Mosquitto configuration, or systemd services.
- Creating, migrating, or changing Supabase telemetry tables.
- Running physical-world procedures that could affect live biome conditions.

## Allowed Without Live Approval When In Scope

These are normally safe if they do not alter live systems:

- Reading files.
- Editing documentation, memory, playbooks, or reference material after stating intended changes and respecting write mode.
- Building firmware with `pio run` without upload.
- Running unit tests.
- Running telemetry coordinator dry-runs or local snapshot output.
- Reading logs or subscribing to MQTT read-only when the user has scoped observation/troubleshooting and no commands are published.

## Firmware Safety

- Missing sensor values must remain valid JSON `null`.
- Avoid blocking loops that can starve OTA or telemetry handling.
- Preserve local safe-state behavior: ESP32 nodes regulate from last known target if higher-level surfaces are unavailable.
- Do not centralize direct pump actuation in the App, website, or Wyse unless explicitly scoped and approved.

## Database Safety

- Do not create dummy Supabase writes to inspect behavior.
- Read source, schema, or existing records before proposing writes.
- Supabase telemetry schema changes need explicit approval and should be coordinated with App/Web consumers.

## Closeout Safety Statement

Every Hardware session should report whether firmware, live controls, MQTT publishing, OTA upload, router/Wyse config, Supabase schema, or physical hardware were changed. If none were changed, say so plainly.
