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

- **Board:** ESP32 (`esp32dev`)
- **Framework:** Arduino via PlatformIO
- **Sensors:** SHT4x (temperature + humidity, I2C, single-node wiring per biome)
- **Network:** Opal GL-SFT1200 micro-router (2.4 GHz biome network), upstream 5 GHz
- **Control bus:** MQTT broker on Dell Wyse 3040 thin client
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
