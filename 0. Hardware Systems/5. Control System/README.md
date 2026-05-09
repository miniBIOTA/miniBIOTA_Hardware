# Control System

## Definition

The Control System is the ESP32 nodes, sensors, local displays, MQTT broker, Dell Wyse thin client, Opal micro-network, telemetry coordinator, and firmware behaviors that form miniBIOTA's distributed nervous system.

## Current Deployment

- One PlatformIO/Arduino ESP32 project per biome.
- Biomes 2-5 are deployed as full sensor nodes with local PWM pump control.
- Biome 1 has WiFi/OTA/MQTT firmware but no sensors installed yet.
- Biome 6 is currently the Wave & Tide System controller and is not part of the sensor telemetry set.
- Mosquitto broker runs on the Dell Wyse 3040 at `192.168.8.228:1883`.
- Local network is the Opal GL-SFT1200 `mB2.4` micro-network.

## Sensor Naming Note

Public and older strategy language may say SHT4x is the production standard. Current deployed sensor nodes use SHT31-D modules. Treat SHT4x as future/production-standard language unless the affected hardware and firmware have actually been upgraded.

## System Boundary

Included here:

- ESP32 nodes and breakout boards.
- Air temperature/humidity sensors.
- DS18B20 probes as control inputs.
- OLED status displays.
- MOSFET pump-control electronics where they are part of the node control path.
- WiFi, OTA, MQTT, Opal, Wyse, Mosquitto, and telemetry coordinator behavior.

Shared with Climate System:

- Pump switching and coolant probe readings affect climate delivery.
- Hardware architecture should be cross-linked rather than duplicated.

## Files

| File | Purpose |
|---|---|
| `sensor-nodes.md` | Biome 2-5 sensor node hardware pattern |
| `control-network.md` | Opal/Wyse/Mosquitto network overview |
| `mqtt-topics.md` | MQTT topic map and live-control boundary |

