---
id: climate_and_rain_system
title: Climate and Rain System
domain: engineering_and_hardware
last_updated: 2026-04-03
tags: [climate, cooling, rain, condensation, cloud-reservoirs, chiller]
---
# Climate and Rain System

The cooling loop and rain generation mechanism that drives the miniBIOTA atmospheric water cycle.

---

## Cooling Loop (Climate System)

### Coolant
- Water + glycol mixture.

### Chiller
- Laboratory-grade "Flask Chiller."
- Operates as a closed coolant loop.

### Architecture
- One shared chilled loop.
- Each atmosphere has its own 12 V pump.
- Each pump taps into the central loop.
- Coolant circulates through heat exchanger mounted on rear exterior glass.

### Control
- Actively controlled, not constant flow.
- Regulated by ESP32 thermostat logic.

---

## Rain Generation Mechanism (Rain System)

### Condensation
- Warm humid air rises into atmospheres.
- Rear glass is chilled via heat exchanger.
- Water vapor condenses on cooled interior surface.
- Condensate flows downward via gravity.

### Cloud Reservoirs
Each atmosphere contains:
- Four triangular prism reservoirs ("clouds").
- Fulcrum pivot with nylon-glass bearing.
- Gravity-driven tipping mechanism.

### Rain Cadence
- When water mass shifts center of gravity, reservoir tips and rain is released into biome below.
- Adjacent clouds may destabilize and tip sequentially.
- Observed cadence: rain approximately every 2 to 3 weeks.
- Variable depending on climate settings and ambient conditions.

---

## Temperature Behavior
- Biomes: 80 F to 90+ F.
- Atmospheres: often near 70 F but variable.
- Coolant may approach near-freezing temperatures.
- Interior atmosphere temperature fluctuates constantly due to humid exhaust inflow.
- Atmosphere temperature is dynamic, not fixed.
