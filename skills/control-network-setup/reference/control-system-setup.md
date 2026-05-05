---
id: control_system_setup_reference
title: Control System Setup Reference
domain: engineering_and_hardware
last_updated: 2026-05-05
tags: [control, esp32, mqtt, wyse, opal, setup, deployment]
---
# Control System Setup Reference

Complete rebuild reference for the miniBIOTA distributed control system. Follow in order from scratch when a rebuild is explicitly scoped.

## Overview

The control system has three layers:

1. Opal GL-SFT1200 router: hosts the isolated local network.
2. Dell Wyse 3040 thin client: runs Mosquitto and telemetry services.
3. Six ESP32 nodes: one per biome.

## Part 1 - Opal Router

### Hardware

- GL.iNet GL-SFT1200 Opal travel router.
- WISP mode.
- 5 GHz radio connects upstream to building WiFi.
- 2.4 GHz radio broadcasts the local biome network.

### Configuration

- Local SSID: `mB2.4`.
- Local WiFi password: stored in this repo's legacy setup reference and should not be repeated in short summaries.
- Admin panel: `192.168.8.1`.
- Wyse 3040 static lease: MAC `8C:47:BE:19:2C:12` -> `192.168.8.228`.

### Static DHCP Leases

| Device | MAC | IP |
|---|---|---|
| wyse3040 | 8C:47:BE:19:2C:12 | 192.168.8.228 |
| biome1-lake | C0:5D:89:DF:48:CC | 192.168.8.103 |
| biome2-lakeshore | 08:A6:F7:6D:E6:38 | 192.168.8.152 |
| biome3-meadow | 6C:C8:40:43:C1:C8 | 192.168.8.122 |
| biome4-mangrove | 6C:C8:40:72:CA:A4 | 192.168.8.212 |
| biome5-marine | 1C:69:20:EA:44:D0 | 192.168.8.185 |
| biome6-seagrass | 6C:C8:40:43:44:84 | 192.168.8.229 |

## Part 2 - Wyse 3040 MQTT Broker

### Hardware

- Dell Wyse 3040 thin client.
- Ethernet to Opal router.
- BIOS set to power on after AC loss.

### OS Installation

1. Download Ubuntu Server 24.04 LTS.
2. Flash to USB with Rufus: GPT target, UEFI.
3. Enter Wyse BIOS with F2, disable Secure Boot, enable USB boot.
4. Install to internal eMMC, usually `/dev/mmcblk0`.
5. During install, set hostname `wyse3040`, username `minibiota`, and enable OpenSSH server.
6. Remove USB and boot to Ubuntu.

### Mosquitto Setup

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y mosquitto mosquitto-clients
sudo systemctl enable mosquitto
sudo systemctl start mosquitto
```

Mosquitto config:

```conf
listener 1883
allow_anonymous true
persistence true
persistence_location /var/lib/mosquitto/
log_dest file /var/log/mosquitto/mosquitto.log
include_dir /etc/mosquitto/conf.d
```

Restart/check:

```bash
sudo systemctl restart mosquitto
sudo systemctl status mosquitto
```

SSH:

```bash
ssh minibiota@192.168.8.228
```

Read-only MQTT verification on the Wyse:

```bash
mosquitto_sub -h localhost -t "miniBIOTA/biome/2/telemetry"
```

## Part 3 - ESP32 Nodes

### Hardware

- Module: ESP-WROOM-32 / ESP32-DevKitC.
- Carrier board: ESP32 breakout board with screw-terminal GPIO expansion.
- Toolchain: PlatformIO in VS Code.

### First Flash

USB required:

```powershell
pio run -e esp32dev -t upload --upload-port COMX --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

### Future Flashes

OTA:

```powershell
pio run -e esp32dev_ota -t upload --project-dir "M:\miniBIOTA\miniBIOTA_Hardware\<biome folder>"
```

Do not upload or OTA without explicit approval.

## Part 4 - MQTT Topic Structure

| Topic | Direction | Payload |
|---|---|---|
| `miniBIOTA/biome/<id>/status` | ESP32 -> Wyse | `"online"` on boot |
| `miniBIOTA/biome/<id>/telemetry` | ESP32 -> Wyse | JSON, published every 10 seconds |
| `miniBIOTA/biome/<id>/setpoint` | Wyse/App -> ESP32 | Float string such as `"22.5"` |

Telemetry payload for biomes 2-5:

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

Publishing to a setpoint topic changes live control state and requires explicit approval.

## Part 5 - Adding A New Node

1. Flash WiFi + OTA + MQTT firmware via USB first.
2. Open serial monitor and note the IP received from Opal.
3. Update `upload_port` in `platformio.ini`.
4. Set static DHCP lease in Opal admin.
5. Use OTA for future flashes.

## Pending / Next Steps

- Freshwater Lake: wire DS18B20 temperature probe and add sensor code.
- Seagrass: add MQTT controls for wave rhythm and amplitude.
- Biomes 2-5: rewire using XT30 power and JST-XH 2.54mm signal connectors.
- Deploy/configure Wyse coordinator service and Supabase `telemetry_snapshot` access.
- History telemetry and setpoint command queues remain deferred.
