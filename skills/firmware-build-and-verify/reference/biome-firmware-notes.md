---
id: biome_firmware_notes
title: Biome Firmware Notes
domain: engineering_and_hardware
last_updated: 2026-05-09
tags: [firmware, platformio, esp32, ota, sensors]
---
# Biome Firmware Notes

## Node Summary

| Biome | Folder | Hostname | Firmware type | App status |
|---|---|---|---|---|
| 1. Freshwater Lake | `1. Freshwater Lake Biome/` | `biome1-lake` | WiFi + OTA + MQTT; no sensors | Offline expected |
| 2. Lakeshore | `2. Lakeshore Biome/` | `biome2-lakeshore` | Full sensor + PWM pump | Atmo SHT31 shows Sensor Err; biome display dim |
| 3. Lowland Meadow | `3. Lowland Meadow Biome/` | `biome3-meadow` | Full sensor + PWM pump | Atmo SHT31 shows Sensor Err over unstable data |
| 4. Mangrove Forest | `4. Mangrove Forest Biome/` | `biome4-mangrove` | Full sensor + PWM pump | Bio SHT31 appears water damaged; biome screen off |
| 5. Marine Shore | `5. Marine Shore Biome/` | `biome5-marine` | Full sensor + PWM pump | Currently working; humidity display artifact |
| 6. Seagrass Meadow | `6. Seagrass Meadow Biome/` | `biome6-seagrass` | Wave/tide stepper + WiFi/OTA on Core 0 | Wave motor only |

## OTA Status

As of 2026-04-25, biomes 1-5 were flashed via USB serial with current firmware, so OTA works going forward. Biome 6 is live as the wave/tide node.

USB upload is for first flash or recovery:

```powershell
pio run -e esp32dev -t upload --upload-port COMX --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

OTA upload is the normal path after current firmware is installed:

```powershell
pio run -e esp32dev_ota -t upload --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

Do not run either upload command without explicit approval.

## Firmware Bugs Fixed 2026-04-25

Three bugs were patched across biomes 1-5:

1. WiFi watchdog: `setup()` had a blocking `while (WiFi.status() != WL_CONNECTED)` loop with no timeout. Fixed with a 30-second timeout and `esp_restart()`.
2. Non-blocking MQTT reconnect: `connectMQTT()` used a blocking retry loop with long delays. Fixed with millis-based single-attempt retries and 5-second backoff.
3. NaN-to-null telemetry serialization: `snprintf` emitted `nan` for failed sensors, which broke JSON parsing. Fixed by substituting JSON `null` for missing float fields.

Preserve these behaviors when editing shared firmware patterns.

## Sensor Node Pin Assignments For Biomes 2-5

| Pin | Function |
|---|---|
| SDA=21, SCL=22 | I2C Bus 1: atmosphere SHT31 + atmosphere OLED |
| SDA=18, SCL=19 | I2C Bus 2: biome SHT31 + biome OLED |
| GPIO 4 | DS18B20 liquid temperature (OneWire) |
| GPIO 27 | PWM pump output |

- I2C speed: 100 kHz for long-cable stability.
- OLED: SSD1306 128x64 at address `0x3C` on each bus.
- SHT31: address `0x44` on each bus.

## PWM Pump Logic

- `TARGET_TEMP_C`: pump off below this target.
- `MAX_TEMP_C`: pump at 100% above this threshold, usually target plus 5 C.
- Between target and max: proportional PWM.
- Kickstart: 255 PWM for a short start pulse when starting from off.
- Setpoints arrive through MQTT on `miniBIOTA/biome/<id>/setpoint`.

Changing this behavior is a live-biosphere control change and requires explicit approval.

## Seagrass Wave Node

- Runs stepper motor wave simulation on Core 1.
- WiFi and ArduinoOTA run as a FreeRTOS task on Core 0.
- No current sensor telemetry role.
- MQTT controls for wave rhythm and amplitude are future work.

## Pending Firmware/Hardware Work

- Freshwater Lake: wire DS18B20 temperature probe and add sensor code when hardware exists.
- Seagrass Meadow: add MQTT controls for wave rhythm and amplitude when scoped.
- Biomes 2-5: rewire sensor/controller harnesses to resolve SHT31 wiring and connection-quality faults. Final connector standard is still open; XT30 power and JST-XH 2.54mm signal connectors are candidates, not settled requirements.
