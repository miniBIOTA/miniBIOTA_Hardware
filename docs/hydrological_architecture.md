---
id: hydrological_architecture
title: Hydrological Architecture
domain: engineering_and_hardware
last_updated: 2026-04-03
tags: [hydrology, freshwater, marine, air-topology, estuary]
---
# Hydrological Architecture

The water routing, air volume topology, and freshwater-marine isolation design of the miniBIOTA system.

---

## Air Volume Topology

miniBIOTA functions as one coupled air network.

### Lake
- Connected to Lakeshore via side port.
- Exhausts humid air via riser pipe to Lakeshore Atmosphere.
- Receives cooled air back through shared connections.

### Seagrass Meadow
- Connected to Beach biome.
- Exhausts humid air via riser pipe to Beach Atmosphere.
- Receives cooled air via shared air volume.

Atmospheres act as processing nodes. The system should be treated as a single shared atmospheric mass with routed processing.

---

## Freshwater Side
- Lake -> Lakeshore -> Grassland
- Connected via surface ports and underground bottom ports.
- Water level equalizes naturally via gravity. No pumps. No overflow devices.

## Marine Side
- Beach <-> Seagrass Meadow
- Saltwater flows freely between the two.
- Marine hydrology is isolated underground from freshwater side.

## Freshwater-Marine Isolation
- Grassland and Mangrove sit at equal elevation.
- Not connected underground. Prevents saltwater intrusion.

## Planned: Engineered Estuary
- Engineered estuary system for controlled density-separated interaction.
- Baffle-controlled flow with continuous freshwater push from rain cycle.
- This is a planned future feature, not current state.
