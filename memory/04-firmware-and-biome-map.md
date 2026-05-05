---
id: hardware_firmware_biome_map
title: Firmware And Biome Map
domain: engineering_and_hardware
last_updated: 2026-05-05
tags: [memory, firmware, platformio, biomes, ota]
---
# Firmware And Biome Map

Hardware firmware is organized as one PlatformIO project per biome folder. Folder numbers match Supabase `biome_id` values.

## Biome Projects

| Folder | Biome | biome_id | Firmware role | Current watchout |
|---|---|---:|---|---|
| `1. Freshwater Lake Biome/` | Freshwater Lake | 1 | WiFi, OTA, MQTT; no sensors yet | Offline expected |
| `2. Lakeshore Biome/` | Lakeshore | 2 | Sensor node + PWM pump | Atmo SHT31 wiring fault returns null |
| `3. Lowland Meadow Biome/` | Lowland Meadow | 3 | Sensor node + PWM pump | Atmo SHT31 intermittent wiring fault |
| `4. Mangrove Forest Biome/` | Mangrove Forest | 4 | Sensor node + PWM pump | Bio SHT31 wiring fault returns null |
| `5. Marine Shore Biome/` | Marine Shore | 5 | Sensor node + PWM pump | Bio SHT31 wiring fault returns null |
| `6. Seagrass Meadow Biome/` | Seagrass Meadow | 6 | Wave/tide stepper + WiFi/OTA | Sensor telemetry not part of current node role |

## Firmware Status

- Biomes 1-5 were USB-flashed on 2026-04-25; OTA works going forward.
- Biome 6 is live as the wave/tide node.
- Missing sensor values must serialize as JSON `null`, not `nan`.
- WiFi connection must retain a timeout/restart path rather than hanging forever.
- MQTT reconnect must stay non-blocking enough for telemetry and OTA handling.

## Commands

Build:

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

Do not run USB or OTA upload commands without explicit user approval.

## Approval Boundary

Ask before changing firmware that touches:

- Pump switching or PWM behavior.
- Thermostat logic or hysteresis.
- Setpoint parsing or MQTT control topics.
- OTA behavior.
- WiFi/MQTT connection behavior.
- Telemetry serialization or schema.
- Anything that can affect live biome conditions.

## Exact References

Use `skills/firmware-build-and-verify/reference/biome-firmware-notes.md` for detailed node status, pin assignments, OTA notes, and firmware bug history.
