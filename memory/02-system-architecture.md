---
id: hardware_system_architecture
title: System Architecture
domain: engineering_and_hardware
last_updated: 2026-05-09
tags: [memory, architecture, enclosure, climate, rain, hydrology]
---
# System Architecture

miniBIOTA is a modular closed ecological biosphere made from six connected biome tanks plus atmosphere processors, external energy/control systems, and a local control network.

## Physical Shape

- Six 29-gallon biome tanks form the main ecological sequence.
- Four vertically mounted 29-gallon atmosphere tanks sit above Lakeshore, Lowland Meadow, Mangrove Forest, and Marine Shore.
- Freshwater Lake and Seagrass Meadow exhaust humid air into adjacent atmosphere processors rather than having their own atmosphere tanks.
- Custom plywood cabinets set intentional elevation differences across the biomes.
- Biomes use drilled 3-inch ports, Fernco rubber PVC couplers, rigid PVC sections, and bottom/top/side bulkhead routing.

## Biome Sequence

Left to right:

1. Freshwater Lake
2. Lakeshore
3. Lowland Meadow
4. Mangrove Forest
5. Marine Shore
6. Seagrass Meadow

Legacy documents may call Lowland Meadow "Grassland" and Marine Shore "Beach." Use the repo's current biome names for firmware, App, Web, Content, and Brain coordination.

## Closure Boundary

Current state:

- Minor passive air leakage exists.
- No routine feeding, nutrient supplementation, filtration, or mechanical correction.
- Organisms may still be added or removed for experimental refinement.
- Water is not routinely added.

Target state:

- No gas, liquid, or solid matter crosses the system boundary.
- Only energy crosses as light and externally imposed thermal gradients.
- Biological energy comes from internal cycling and photosynthesis.

## Hydrology

- Freshwater side: Freshwater Lake -> Lakeshore -> Lowland Meadow.
- Marine side: Marine Shore <-> Seagrass Meadow.
- Freshwater and marine underground hydrology are isolated.
- Lowland Meadow and Mangrove sit at equal elevation but are not connected underground, preventing saltwater intrusion.
- A controlled engineered estuary is a future feature, not current state.

## Air Topology

Treat miniBIOTA as one coupled air network with routed processing:

- Lake connects to Lakeshore and exhausts humid air through a riser pipe into the Lakeshore atmosphere.
- Seagrass connects to Marine Shore and exhausts humid air into the Marine Shore atmosphere.
- Atmospheres condense, cool, and route water back into the biomes.

## Climate And Rain Systems

- The Climate System uses a shared water/glycol coolant loop, lab flask chiller, one 12 V pump per atmosphere/biome branch, and rear-glass heat exchangers.
- Cooling is actively controlled by ESP32 thermostat logic, not constant-flow by default.
- Warm humid air condenses on cooled glass and drains into cloud reservoirs.
- Each atmosphere has four triangular prism cloud reservoirs with gravity-driven tipping.
- Observed rain cadence is roughly every 2-3 weeks, depending on settings and ambient conditions.

## Exact References

Use `0. Hardware Systems/` for detailed system-level architecture:

- `0. Hardware Systems/1. Climate System/`
- `0. Hardware Systems/2. Rain System/`
- `0. Hardware Systems/3. Lighting System/`
- `0. Hardware Systems/4. Wave & Tide System/`
- `0. Hardware Systems/5. Control System/`
- `0. Hardware Systems/6. Enclosure/`

Use `skills/hardware-architecture-reference/reference/` only for older architecture reference context that has not yet been promoted into `0. Hardware Systems/`.
