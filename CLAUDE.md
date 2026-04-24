# miniBIOTA Hardware — Claude Context

## What This Repo Is

ESP32 firmware for per-biome sensor nodes in the miniBIOTA closed biosphere. One PlatformIO project per biome, Arduino framework.

## Project Structure

| Folder | Biome | Supabase biome_id |
|---|---|---|
| `1. Freshwater Lake Biome/` | Freshwater Lake | 1 |
| `2. Lakeshore Biome/` | Lakeshore | 2 |
| `3. Lowland Meadow Biome/` | Lowland Meadow | 3 |
| `4. Mangrove Forest Biome/` | Mangrove Forest | 4 |
| `5. Marine Shore Biome/` | Marine Shore | 5 |
| `6. Seagrass Meadow Biome/` | Seagrass Meadow | 6 |

## Platform

- **Module:** ESP-WROOM-32 (ESP32-DevKitC), all 6 nodes
- **Carrier board:** ESP32 Breakout Board with 3.5mm screw terminal GPIO expansion (0.9"/1.0" form factor)
- **Framework:** Arduino via PlatformIO
- **Sensors:** SHT31 (temperature + humidity, I2C) — deployed on biomes 2–5; biome 1 pending hardware
- **Network:** Opal GL-SFT1200 micro-router (2.4 GHz biome network `mB2.4`), upstream 5 GHz
- **MQTT broker:** Mosquitto on Dell Wyse 3040 thin client at `192.168.8.228:1883`
- **Each ESP32 owns:** local thermostat hysteresis, 12 V pump switching, sensor publishing

## How the Control System Works

The Dell Wyse publishes target temperature setpoints via MQTT. Each ESP32 subscribes, owns local PID/hysteresis logic, and publishes telemetry back. The system stays operational if upstream internet fails — control is local.

## Cross-References

For strategy, ecology, and system architecture context, read:
- `M:\miniBIOTA\miniBIOTA_Brain\_system\agent_memory.md`
- `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\engineering_and_hardware_overview.md`
- `M:\miniBIOTA\miniBIOTA_Brain\6. Engineering & Hardware\control_network.md`

## Write Policy

Follow the cautious write model from Brain (`agent_memory.md`). Confirm writes with Josue before modifying firmware that touches pump switching or thermostat logic — those affect live ecology.
