---
id: control_network
title: Control Network
domain: engineering_and_hardware
last_updated: 2026-04-03
tags: [control, esp32, mqtt, opal, sensors, distributed, thin-client]
---
# Control Network

The distributed control, telemetry, and sensor architecture for miniBIOTA.

---

## Micro-Network

### Central Hub
- GL.iNet GL-SFT1200 (Opal) travel router running in WISP (Wireless Client Router) mode.

### Radio Split
- 5 GHz radio connects upstream to building WiFi for internet access.
- 2.4 GHz radio broadcasts the isolated local network (e.g., `miniBIOTA_Local`).

### Network Roles
- The Opal acts as DHCP server for the local network.
- All ESP32 nodes connect only to the Opal-hosted local network.
- The Dell Wyse 3040 thin client connects only to the same local network.
- ESP32 nodes and the thin client do not connect directly to building WiFi.

### Resilience
- If building internet fails, the Opal-hosted local network remains operational.
- ESP32 nodes continue to publish MQTT data locally.
- The thin client continues to receive and log telemetry locally.

---

## ESP32 Control Nodes

Each ESP32 node:
- Owns the local thermostat loop for its biome.
- Applies hysteresis locally.
- Switches its assigned 12 V cooling pump on and off locally.
- Maintains target temperature setpoints received over MQTT.
- Continues regulating from the last known target temperature if the thin client is unavailable (local safe state).
- Reads SHT4x air temperature/humidity sensors.
- Reads coolant temperature probes.
- Will soon control lighting schedule.

---

## Dell Wyse 3040 Thin Client (Local MQTT Coordinator)

- Acts as the local MQTT/logging coordinator on the micro-network.
- Publishes setpoint updates. Does not directly command pump ON/OFF states.
- Relies on built-in eMMC storage to absorb high-frequency SHT4x telemetry writes without MicroSD flash burnout.
- Hardwired by Ethernet to the Opal router for zero-latency broker stability.

---

## Web Dashboard
- Adjusts target temperatures through the thin client/MQTT layer.
- Does not directly actuate pumps.
- Should be treated as a setpoint and observability surface, not centralized actuator control.

---

## Sensors

### Installed (Production Standard)
- SHT4x air temperature/humidity sensors on terrestrial biomes and atmospheres.
- Coolant temperature probes on heat exchangers.
- Note: SHT31-D units are prototype-era hardware — treat as legacy reference only.

### Node Wiring Topology
- Each control node uses a single I2C bus.
- The earlier dual-bus approach is legacy and not the active standard.
- Single-bus topology simplifies wiring, troubleshooting, and field maintenance.

### Planned Sensors
- CO2, Oxygen, Methane, Possible pH, Possible salinity, Additional dissolved parameters.

---

## Other Control Systems

### Wave & Tide System
- Stepper motor, rotary encoder, mechanical swash motion.

### Lighting System
- Currently external timer. Future ESP32 integration planned.

### Interface
- 1-inch OLED display per node.
- Local logging remains available even if building internet is unavailable.
