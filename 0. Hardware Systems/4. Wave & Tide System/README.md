# Wave & Tide System

## Definition

The Wave & Tide System is the stepper motor and mechanical swash system that simulates tidal motion on the marine side.

## Current Deployment

- Current controller: Biome 6 Seagrass Meadow ESP32 node.
- Current firmware role: standalone wave/tide stepper node with WiFi/OTA; MQTT control is future work.
- Current mechanical role: vertically oscillates a water-filled PVC chamber to pump water in and out of the Seagrass Meadow.

## System Boundary

Included here:

- Stepper motor.
- Motor driver.
- Encoder feedback.
- Linear rail, belt drive, chamber, and external mechanical motion assembly.
- Wave and tide simulation profiles.

Not included here:

- Sensor-node telemetry for Biomes 2-5, which belongs to the Control System.
- Marine hydrology and organism response, which belongs in hydrology/research context.

## Files

| File | Purpose |
|---|---|
| `mechanical-swash.md` | Mechanical motion system summary |
| `stepper-control.md` | Motor driver, encoder, and firmware control summary |

## Detailed Installed Spec

The current installed hardware spec remains in `../../6. Seagrass Meadow Biome/biome_hardware.md`.
