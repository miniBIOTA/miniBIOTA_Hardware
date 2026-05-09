# Control Network

## Current Architecture

The local control network has three layers:

1. Opal GL-SFT1200 router hosts the isolated biome WiFi network.
2. Dell Wyse 3040 thin client runs Mosquitto and telemetry services.
3. ESP32 nodes connect over WiFi and publish/subscribe MQTT.

## Network Hardware

- Router: GL.iNet GL-SFT1200 Opal.
- Local SSID: `mB2.4`.
- Broker host: Dell Wyse 3040 at `192.168.8.228`.
- Broker port: `1883`.
- Wyse connects to Opal by Ethernet.

## Node Model

Each ESP32 node owns its local loop:

- Reads sensors.
- Publishes telemetry.
- Subscribes to setpoint updates where implemented.
- Regulates local pump behavior from last known target.
- Continues local regulation if higher-level software is unavailable.

## Exact Setup Reference

Use `skills/control-network-setup/reference/control-system-setup.md` for static leases, setup commands, and rebuild details.

