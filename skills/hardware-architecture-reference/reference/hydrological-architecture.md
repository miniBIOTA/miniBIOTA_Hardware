---
id: hydrological_architecture_reference
title: Hydrological Architecture Reference
domain: engineering_and_hardware
last_updated: 2026-05-09
tags: [hydrology, freshwater, marine, air-topology, estuary]
---
# Hydrological Architecture Reference

The miniBIOTA hydrological architecture covers water routing, air volume topology, and freshwater-marine isolation.

System-level hardware details now live under `0. Hardware Systems/`; use this file as compact supporting hydrology context.

## Air Volume Topology

miniBIOTA functions as one coupled air network.

### Freshwater Lake

- Connected to Lakeshore via side port.
- Exhausts humid air by riser pipe to the Lakeshore atmosphere.
- Receives cooled air back through shared connections.

### Seagrass Meadow

- Connected to Marine Shore.
- Exhausts humid air by riser pipe to the Marine Shore atmosphere.
- Receives cooled air through shared air volume.

Atmospheres act as processing nodes. Treat the system as a shared atmospheric mass with routed processing.

## Freshwater Side

- Freshwater Lake -> Lakeshore -> Lowland Meadow.
- Connected by surface ports and underground bottom ports.
- Water level equalizes naturally by gravity.
- No pumps.
- No overflow devices.

## Marine Side

- Marine Shore <-> Seagrass Meadow.
- Saltwater flows freely between the two.
- Marine hydrology is isolated underground from the freshwater side.

## Freshwater-Marine Isolation

- Lowland Meadow and Mangrove Forest sit at equal elevation.
- They are not connected underground.
- This prevents saltwater intrusion into the freshwater side.

## Planned Engineered Estuary

An engineered estuary is planned but not current state. Concept:

- Controlled density-separated interaction.
- Baffle-controlled flow.
- Continuous freshwater push from rain cycle.

Do not describe the engineered estuary as active unless it has been built.
