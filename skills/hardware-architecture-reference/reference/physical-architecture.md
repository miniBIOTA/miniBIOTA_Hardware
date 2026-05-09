---
id: physical_architecture_reference
title: Physical Architecture Reference
domain: engineering_and_hardware
last_updated: 2026-05-09
tags: [architecture, tanks, cabinets, ports, bulkheads, modular]
---
# Physical Architecture Reference

Active Enclosure details now live in `systems/06-enclosure/`. Keep this file as compact supporting context for the architecture playbook.

## Core Definition

miniBIOTA is a modular, closed ecological biosphere system composed of multiple interconnected biomes housed in 29-gallon glass tanks. It simulates atmospheric exchange, water cycling, nutrient cycling, trophic interactions, and long-term ecological succession without external filtration or feeding once sealed.

## Closure Definition

### Current State

- Minor passive air leakage exists.
- No feeding occurs.
- No nutrient supplementation occurs.
- No filtration or mechanical correction is present.
- Organisms are occasionally added or removed for experimental refinement.
- Water is not routinely added.

### Target State

- Fully airtight.
- No gas exchange with room.
- No water addition or removal.
- No feeding.
- No organism introduction.
- Only energy input via light through glass.

### Closure Defined

- Mechanically: no gas, liquid, or solid matter entering or exiting the system.
- Biologically: all trophic energy derived from internal cycling and photosynthesis.
- Chemically: all elemental cycles contained within system boundaries.

## System Boundaries

### Included

- All six biome tanks.
- All four atmosphere tanks.
- All internal air volumes.
- All internal water volumes.
- All soil and substrate.
- All organisms.
- All condensation surfaces.
- All rain reservoirs.
- All sealed ports and couplers.

### Excluded

- External lighting fixtures.
- Electrical control systems.
- Chiller hardware.
- External coolant loop hardware.
- Room air.

Energy crosses the boundary as light. Thermal gradients are externally influenced but internally expressed. Mass is not intended to cross the boundary in final configuration.

## Structural Support System

- Each biome tank is supported by a custom plywood cabinet with enclosed front doors.
- Height varies by biome, creating intentional vertical staggering.
- Elevation hierarchy: Freshwater Lake < Lakeshore < Lowland Meadow = Mangrove Forest > Marine Shore > Seagrass Meadow.
- Elevation staging supports surface water continuity, convection-driven airflow, terrain gradient, and hydrological flow logic.

## Atmosphere Mounting System

- Each atmosphere tank is a vertically oriented 29-gallon glass tank mounted above a terrestrial/coastal biome.
- Atmospheres are mounted above Lakeshore, Lowland Meadow, Mangrove Forest, and Marine Shore.
- Atmospheres are atmospheric processing chambers, not separate biomes.
- Freshwater Lake and Seagrass Meadow route humid air to adjacent atmosphere processors.

## Modular Architecture

- Each biome has two left ports, two right ports, one bottom port, and three top ports, all 3-inch.
- Ports are permanently drilled bulkheads.
- Connections use 3-inch Fernco rubber PVC couplers and rigid PVC segments.
- The system is modular and expandable. Rearrangement requires draining and resealing.

## Biome Configuration

Left to right:

1. Freshwater Lake
2. Lakeshore
3. Lowland Meadow
4. Mangrove Forest
5. Marine Shore
6. Seagrass Meadow

Legacy wording may say Grassland for Lowland Meadow and Beach for Marine Shore.
