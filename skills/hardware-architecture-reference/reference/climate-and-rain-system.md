---
id: climate_and_rain_system_reference
title: Climate And Rain System Reference
domain: engineering_and_hardware
last_updated: 2026-05-05
tags: [climate, cooling, rain, condensation, cloud-reservoirs, chiller]
---
# Climate And Rain System Reference

The Climate System and Rain System drive the miniBIOTA atmospheric water cycle.

## Climate System

### Coolant

- Water + glycol mixture.

### Chiller

- Laboratory-grade flask chiller.
- Operates as a closed coolant loop.

### Architecture

- One shared chilled loop.
- Each atmosphere or cooling branch has its own 12 V pump.
- Each pump taps into the central loop.
- Coolant circulates through a heat exchanger mounted on rear exterior glass.

### Control

- Actively controlled, not constant-flow by default.
- Regulated by ESP32 thermostat logic.
- Firmware changes to thermostat or pump behavior require explicit approval.

## Rain System

### Condensation

- Warm humid air rises into atmospheres.
- Rear glass is chilled by the heat exchanger.
- Water vapor condenses on the cooled interior surface.
- Condensate flows downward by gravity.

### Cloud Reservoirs

Each atmosphere contains:

- Four triangular prism reservoirs, called clouds.
- Fulcrum pivot with nylon-glass bearing.
- Gravity-driven tipping mechanism.

### Rain Cadence

- When water mass shifts the center of gravity, a reservoir tips and releases rain into the biome below.
- Adjacent clouds may destabilize and tip sequentially.
- Observed cadence is roughly every 2-3 weeks.
- Cadence varies with climate settings and ambient conditions.

## Temperature Behavior

- Biomes often run 80 F to 90+ F.
- Atmospheres are often near 70 F but variable.
- Coolant may approach near-freezing temperatures.
- Interior atmosphere temperature fluctuates because of humid exhaust inflow.
- Atmosphere temperature is dynamic, not fixed.
