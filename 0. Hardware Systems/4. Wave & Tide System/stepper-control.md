# Stepper Control

## Current Electrical Hardware

- Microcontroller: ESP32-DevKitC-VIE.
- Stepper motor: Nema 23, 3 Nm.
- Motor driver: DM542.
- Microstepping: 1600 pulse/rev.
- Peak current setting: documented as 4.2 A, pending verification against DM542 switch table.
- Feedback sensor: Taiss incremental encoder, optical AB 2-phase quadrature, 600 P/R, 5-24 V, 6 mm shaft.
- Logic supply: Mean Well LRS-350-12 through Dorhea buck converter to ESP32 5 V.
- Motor supply: Aclorol 36 V / 10 A direct to DM542 V+.

## Current Control Model

- Positioning uses encoder feedback.
- Physical limit switches have been removed.
- Wave profile: higher frequency, lower amplitude.
- Tide profile: lower frequency, higher amplitude.
- MQTT control is planned but not implemented in current deployed firmware.

## Installed Spec

See `../../6. Seagrass Meadow Biome/biome_hardware.md` for pin assignments, DM542 DIP switch settings, and full wiring diagram.
