---
id: control_system_setup
title: Control System Setup Guide
domain: engineering_and_hardware
last_updated: 2026-04-25
tags: [control, esp32, mqtt, wyse, opal, setup, deployment]
---

# Control System Setup Guide

Complete rebuild guide for the miniBIOTA distributed control system. Follow in order from scratch.

---

## Overview

The control system has three layers:
1. **Opal GL-SFT1200 router** — hosts the isolated local network all devices connect to
2. **Dell Wyse 3040 thin client** — runs the MQTT broker (Mosquitto), logs telemetry
3. **6 × ESP32 nodes** — one per biome, own local sensor reading, pump control, and OTA updates

---

## Part 1 — Opal Router

### Hardware
- GL.iNet GL-SFT1200 (Opal) travel router
- Running in WISP (Wireless Client Router) mode
- 5 GHz radio connects upstream to building WiFi
- 2.4 GHz radio broadcasts the local biome network

### Configuration
- **Local SSID:** `mB2.4`
- **Local WiFi password:** `qYKEQe8R763HKmk`
- **Admin panel:** `192.168.8.1` (default GL.iNet address)
- **Admin password:** stored separately (default factory password: `goodlife`)
- **Wyse 3040 static lease:** MAC `8C:47:BE:19:2C:12` → `192.168.8.228`

### Static DHCP leases (set in Opal admin → Clients)
| Device | MAC | IP |
|---|---|---|
| wyse3040 | 8C:47:BE:19:2C:12 | 192.168.8.228 |
| biome1-lake | C0:5D:89:DF:48:CC | 192.168.8.103 |
| biome2-lakeshore | 08:A6:F7:6D:E6:38 | 192.168.8.152 |
| biome3-meadow | 6C:C8:40:43:C1:C8 | 192.168.8.122 |
| biome4-mangrove | 6C:C8:40:72:CA:A4 | 192.168.8.212 |
| biome5-marine | 1C:69:20:EA:44:D0 | 192.168.8.185 |
| biome6-seagrass | 6C:C8:40:43:44:84 | 192.168.8.229 |

---

## Part 2 — Wyse 3040 (MQTT Broker)

### Hardware
- Dell Wyse 3040 thin client
- Connected via Ethernet to Opal router (not WiFi)
- BIOS set to power on after AC loss

### OS Installation
1. Download Ubuntu Server 24.04 LTS (`ubuntu-24.04.x-live-server-amd64.iso`)
2. Flash to USB with Rufus (partition: GPT, target: UEFI)
3. Enter Wyse BIOS (F2 at boot), disable Secure Boot, enable USB boot
4. Boot USB and install to internal eMMC (`/dev/mmcblk0`)
5. During install: set hostname `wyse3040`, username `minibiota`, enable OpenSSH server
6. After install: remove USB, boot to Ubuntu login prompt

### Mosquitto Setup
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

Edit `/etc/mosquitto/mosquitto.conf`:
```
listener 1883
allow_anonymous true
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
include_dir /etc/mosquitto/conf.d
```

```bash
sudo systemctl restart mosquitto
sudo systemctl status mosquitto  # should show active (running)
```

### BIOS settings
- Power on after AC loss: enabled
- System password: none (remove if present — blocks headless boot)
- USB boot: can be disabled after OS is installed

### Accessing the Wyse
```bash
ssh minibiota@192.168.8.228
```

### Verifying MQTT is receiving data
```bash
mosquitto_sub -h localhost -t "miniBIOTA/biome/2/telemetry"
```

---

## Part 3 — ESP32 Nodes

### Hardware
- **Module:** ESP-WROOM-32 (ESP32-DevKitC)
- **Carrier board:** ESP32 Breakout Board with 3.5mm screw terminal GPIO expansion
- **Toolchain:** PlatformIO in VS Code

### First flash (USB required)
```bash
pio run -e esp32dev -t upload --upload-port COMX --project-dir "m:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

### All future flashes (OTA, wireless)
```bash
pio run -e esp32dev_ota -t upload --project-dir "m:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

### Node firmware summary

| Biome | Folder | Hostname | Firmware type | App status |
|---|---|---|---|---|
| 1. Freshwater Lake | `1. Freshwater Lake Biome/` | biome1-lake | WiFi + OTA + MQTT (no sensors) | Offline (expected) |
| 2. Lakeshore | `2. Lakeshore Biome/` | biome2-lakeshore | Full sensor + PWM pump | Healthy — atmo SHT31 null (wiring fault) |
| 3. Lowland Meadow | `3. Lowland Meadow Biome/` | biome3-meadow | Full sensor + PWM pump | Healthy — atmo SHT31 intermittent (wiring fault) |
| 4. Mangrove Forest | `4. Mangrove Forest Biome/` | biome4-mangrove | Full sensor + PWM pump | Healthy — bio SHT31 null (wiring fault) |
| 5. Marine Shore | `5. Marine Shore Biome/` | biome5-marine | Full sensor + PWM pump | Healthy — bio SHT31 null (wiring fault, loose wire fixed) |
| 6. Seagrass Meadow | `6. Seagrass Meadow Biome/` | biome6-seagrass | Wave/tide stepper + WiFi/OTA on Core 0 | N/A — wave motor only |

**OTA status (as of 2026-04-25):** All 5 sensor biomes (1–5) flashed via USB serial on 2026-04-25. Framework is now current — OTA works going forward. Biome 6 (Seagrass) has not been reflashed via USB; OTA from prior version should still work.

### Firmware bugs fixed (2026-04-25, commit 1927fb7)

Three bugs patched across biomes 1–5:

1. **WiFi watchdog** — `setup()` had a blocking `while (WiFi.status() != WL_CONNECTED)` loop with no timeout. If the board missed the AP association window on boot, it hung forever. Fixed: 30-second timeout with `esp_restart()`.

2. **Non-blocking `connectMQTT()`** — the reconnect function used a blocking `while (!mqtt.connected())` with `delay(5000)` per retry. This froze the sketch during MQTT reconnect, silencing telemetry and blocking `ArduinoOTA.handle()`. Fixed: millis()-based single-attempt per `loop()` call with 5-second backoff.

3. **NaN → null in telemetry JSON** — `snprintf` with `%.2f` on a NaN float outputs the literal string `nan`, which is invalid JSON. `JSON.parse()` in the Electron app was silently dropping every packet from boards with failed sensors, making them appear offline in the Monitoring tab even though they were publishing. Fixed: each float field checks `isnan()` and substitutes `null`. This was why only biome 3 showed in the app at session start — biomes 2 and 4 consistently published NaN on one sensor.

### Sensor node pin assignments (biomes 2–5)
| Pin | Function |
|---|---|
| SDA=21, SCL=22 | I2C Bus 1 — atmosphere SHT31 + atmosphere OLED |
| SDA=18, SCL=19 | I2C Bus 2 — biome SHT31 + biome OLED |
| GPIO 4 | DS18B20 liquid temperature (OneWire) |
| GPIO 27 | PWM pump output |

- I2C speed: 100 kHz (long cable stability)
- OLED: SSD1306 128×64 at address 0x3C on each bus
- SHT31 at address 0x44 on each bus

### PWM pump logic
- `TARGET_TEMP_C` — pump off below this (default 0.0°C)
- `MAX_TEMP_C` — pump at 100% above this (default TARGET + 5.0°C)
- Between target and max: proportional PWM (MIN=40, MAX=255)
- Kickstart: 255 PWM for 250ms when starting from off
- Controlled via MQTT setpoint (see below)

### Seagrass wave node
- Runs stepper motor wave simulation on Core 1
- WiFi + ArduinoOTA run as a FreeRTOS task on Core 0
- No sensor code — wave controls via MQTT planned (future)

---

## Part 4 — MQTT Topic Structure

| Topic | Direction | Payload |
|---|---|---|
| `miniBIOTA/biome/<id>/status` | ESP32 → Wyse | `"online"` on boot |
| `miniBIOTA/biome/<id>/telemetry` | ESP32 → Wyse | JSON, published every 10s |
| `miniBIOTA/biome/<id>/setpoint` | Wyse → ESP32 | Float string e.g. `"22.5"` |

### Telemetry payload (biomes 2–5)
```json
{
  "atmo_t": 24.50,
  "atmo_h": 65.2,
  "bio_t": 26.80,
  "bio_h": 70.1,
  "liq_t": 18.50,
  "pump_pct": 35,
  "target_t": 0.0
}
```

### Setpoint
Publish a plain float string to `miniBIOTA/biome/<id>/setpoint`:
```bash
mosquitto_pub -h localhost -t "miniBIOTA/biome/2/setpoint" -m "22.5"
```
Node sets `TARGET_TEMP_C = 22.5`, `MAX_TEMP_C = 27.5`.

---

## Part 5 — Adding a New Node

1. Flash WiFi + OTA + MQTT firmware via USB first
2. Open serial monitor, note the IP it received from Opal
3. Update `upload_port` in `platformio.ini` to that IP
4. Set static DHCP lease in Opal admin
5. All future flashes via OTA

---

## Pending / Next Steps
- Freshwater Lake (biome 1): wire DS18B20 temp probe, add sensor code
- Seagrass (biome 6): add MQTT controls for wave rhythm and amplitude
- Rewire biomes 2–5 using XT30 (power) + JST-XH 2.54mm (signal) connectors — will resolve all SHT31 NaN wiring faults
- Build Wyse coordinator service + Supabase telemetry tables (Phases 1–3 of `telemetry_pipeline_plan.md`)
- ~~Build Monitoring tab~~ ✓ Done 2026-04-25 — live MQTT to Electron app, all 4 online biomes showing Healthy
