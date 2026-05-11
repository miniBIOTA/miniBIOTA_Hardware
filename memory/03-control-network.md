---
id: hardware_control_network
title: Control Network
domain: engineering_and_hardware
last_updated: 2026-05-11
tags: [memory, control, mqtt, opal, wyse, esp32, sensors]
---
# Control Network

The miniBIOTA control network is a local-first distributed system. ESP32 nodes own local behavior; the Wyse and App observe and coordinate through MQTT.

Active Control System architecture now lives in `0. Hardware Systems/5. Control System/`.

## Network

- Router: GL.iNet GL-SFT1200 Opal in WISP mode.
- Local biome SSID: `mB2.4`.
- Opal admin panel: `192.168.8.1`.
- Dell Wyse 3040 static IP: `192.168.8.228`.
- Mosquitto broker: `192.168.8.228:1883`.
- ESP32 nodes and the Wyse stay on the Opal local network, so local telemetry can continue if building internet fails.
- SSH to the Wyse is enabled for remote maintenance as `minibiota@192.168.8.228` using Josue's PC key at `C:\Users\gimbo\.ssh\minibiota_wyse_ed25519`.

## Node Roles

Each sensor node owns its local loop:

- Reads SHT31 air temperature/humidity sensors.
- Reads DS18B20 liquid temperature where installed.
- Publishes telemetry over MQTT.
- Maintains OTA handling.
- Applies local pump/thermostat behavior from the last known setpoint.
- Does not depend on the App or website for immediate local control.

Biome 6 is different: it is a wave/tide stepper node, with WiFi/OTA on Core 0 and wave motion on Core 1.

## MQTT Topic Pattern

ESP32 nodes use:

- `miniBIOTA/biome/<id>/status`
- `miniBIOTA/biome/<id>/telemetry`
- `miniBIOTA/biome/<id>/setpoint`

Sensor telemetry publishes every 10 seconds where sensors exist. Setpoint topics are live-control surfaces and require explicit user approval before publishing.

## Operator Surfaces

- App Monitoring connects directly to MQTT when on `mB2.4`.
- Wyse coordinator is deployed as an always-on read-only bridge from MQTT to Supabase/website snapshots.
- Website monitoring should remain public read-only.
- Direct pump commands are not the normal control model; setpoints are the operator command surface.

## Wyse Service State

As of 2026-05-11:

- `ssh.service` is active and listening on `0.0.0.0:22`.
- `mosquitto.service` is active and listening on `0.0.0.0:1883`.
- User service `minibiota-telemetry.service` is active under the `minibiota` user and enabled through systemd user linger.
- The service subscribes read-only to `miniBIOTA/biome/+/telemetry` and `miniBIOTA/biome/+/status`, then upserts Supabase `telemetry_snapshot` row `id=1`.

## Current Sensor Standard

Deployed firmware currently uses SHT31 sensors on biomes 2-5. Some older architecture wording mentioned SHT4x as a production standard or future target; do not assume SHT4x is deployed unless the affected firmware or hardware has been changed.

## Exact References

Use `0. Hardware Systems/5. Control System/` for Control System architecture. Use `skills/control-network-setup/reference/` for setup procedures, DHCP leases, Mosquitto configuration, topic tables, payload examples, and deployment steps.
