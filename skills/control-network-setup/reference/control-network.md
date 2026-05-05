---
id: control_network_reference
title: Control Network Reference
domain: engineering_and_hardware
last_updated: 2026-05-05
tags: [control, esp32, mqtt, opal, sensors, distributed, thin-client]
---
# Control Network Reference

The distributed control, telemetry, and sensor architecture for miniBIOTA.

## Micro-Network

### Central Hub

- GL.iNet GL-SFT1200 Opal travel router running in WISP mode.

### Radio Split

- 5 GHz radio connects upstream to building WiFi for internet access.
- 2.4 GHz radio broadcasts the isolated local network.
- Current local SSID: `mB2.4`.

### Network Roles

- The Opal acts as DHCP server for the local network.
- ESP32 nodes connect to the Opal-hosted local network.
- The Dell Wyse 3040 thin client connects to the same local network.
- ESP32 nodes and the Wyse should not need direct building WiFi access.

### Resilience

- If building internet fails, the Opal-hosted local network remains operational.
- ESP32 nodes continue to publish MQTT data locally.
- The Wyse can continue to receive local telemetry.

## ESP32 Control Nodes

Each ESP32 sensor node:

- Owns the local thermostat loop for its biome.
- Switches its assigned 12 V cooling pump locally.
- Maintains target temperature setpoints received over MQTT.
- Continues regulating from the last known target temperature if the thin client is unavailable.
- Reads SHT31 air temperature/humidity sensors in current deployed hardware.
- Reads coolant/liquid temperature probes where installed.
- May later integrate lighting schedule control.

## Dell Wyse 3040 Thin Client

- Acts as the local MQTT/logging coordinator on the micro-network.
- Runs Mosquitto on `192.168.8.228:1883`.
- Publishes setpoint updates only when a user-approved control path is in scope.
- Does not directly command pump ON/OFF states under the normal control model.
- Uses eMMC storage, avoiding MicroSD flash burnout for local logging.
- Is hardwired by Ethernet to the Opal router for broker stability.

## Web Dashboard Boundary

- Adjusts target temperatures only through an approved MQTT/Wyse/Supabase command layer.
- Does not directly actuate pumps.
- Should be treated as a setpoint and observability surface, not centralized actuator control.

## Sensors

### Installed

- SHT31 temperature/humidity sensors on biomes 2-5.
- DS18B20 liquid temperature probes where installed.

### Planned/Future

- CO2.
- Oxygen.
- Methane.
- Possible pH.
- Possible salinity.
- Additional dissolved parameters.

## Other Control Systems

### Wave & Tide System

- Stepper motor, rotary encoder, mechanical swash motion.
- Current node is biome 6 Seagrass Meadow.

### Lighting System

- Currently external timer.
- Future ESP32 integration planned.

### Interface

- 1-inch OLED display per sensor node bus where installed.
- Local logging remains useful even if building internet is unavailable.
