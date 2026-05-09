# Hardware Systems Index

This folder is the system-level hardware architecture layer for miniBIOTA. It mirrors the six public systems used by the website, App media tagging, Brain, and cross-domain planning.

The numbered biome folders remain top-level PlatformIO implementation projects. Use those folders for exact per-biome installed hardware, firmware, and wiring. Use this `systems/` folder for cross-biome subsystem design, shared hardware standards, architecture, and data sheets.

## Canonical Systems

| ID | Folder | System | Purpose |
|---:|---|---|---|
| 1 | `01-climate-system/` | Climate System | Chiller, pumps, plumbing, and heat exchangers that deliver thermal energy to the biosphere |
| 2 | `02-rain-system/` | Rain System | Cloud reservoirs and rain manifolds that collect condensate and distribute rainfall into the biomes |
| 3 | `03-lighting-system/` | Lighting System | Photoperiod and spectrum control that drives photosynthesis across all biomes |
| 4 | `04-wave-and-tide-system/` | Wave & Tide System | Stepper motor and mechanical swash system that simulates tidal motion on the marine side |
| 5 | `05-control-system/` | Control System | ESP32 nodes, sensors, MQTT broker, and Opal micro-network that form the distributed nervous system |
| 6 | `06-enclosure/` | Enclosure | Tanks, cabinets, ports, bulkheads, and sealing architecture that define the physical boundary |

## Routing Rules

- Per-biome installed hardware belongs in the matching biome folder, usually `biome_hardware.md`.
- Cross-biome subsystem architecture belongs in this `systems/` folder.
- Firmware implementation remains in each biome's PlatformIO project.
- Operational playbooks remain in `skills/`.
- Memory files summarize durable context and route to this folder rather than duplicating full specs.

## Current Sensor Naming Note

Public and older strategy language may describe SHT4x sensors as the production standard. Current deployed sensor nodes in Biomes 2-5 use SHT31-D modules. Treat SHT4x as the production/future standard unless the affected hardware and firmware have been upgraded.

