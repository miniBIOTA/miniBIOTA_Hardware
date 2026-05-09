# Climate System

## Definition

The Climate System is the chiller, pumps, plumbing, coolant, heat exchangers, temperature probes, and ESP32 pump-control behavior that deliver thermal energy to the biosphere.

Its current primary job is cooling the rear glass of the four atmosphere tanks so humid internal air condenses and feeds the Rain System.

## Current Deployment

- One shared lab chiller loop circulates a water/glycol coolant mixture.
- Four atmospheric heat exchangers are mounted externally on the rear glass of the four atmosphere tanks.
- Biomes 2-5 each have one BYT-7A015 12 V pump branch and one DS18B20 coolant probe in the heat exchanger.
- Each pump is controlled locally by that biome's ESP32 through a PWM MOSFET module.
- The chiller is currently under repair.

## System Boundary

Included here:

- Lab chiller and coolant loop.
- Water/glycol coolant.
- 12 V circulation pumps for climate branches.
- Atmospheric heat exchangers.
- PEX plumbing and fittings for cooling branches.
- Heat-exchanger coolant temperature probes.
- Pump-control hardware and logic where it affects climate delivery.

Not included here:

- Condensate collection reservoirs and rain distribution, which belong to the Rain System.
- ESP32 network architecture, MQTT broker, OTA, and telemetry as a whole, which belong to the Control System.
- Tanks, cabinets, ports, and sealing, which belong to Enclosure.

## Files

| File | Purpose |
|---|---|
| `atmospheric-heat-exchanger.md` | Detailed spec for the current PVC/glass atmospheric heat exchangers |
| `coolant-loop.md` | Current coolant loop architecture and open details |
| `pumps-and-control.md` | Pump, MOSFET, DS18B20, and ESP32 control relationship |

## Approval Boundary

Changing pump switching, thermostat behavior, setpoint handling, or any live control behavior requires explicit approval because it can alter live biome conditions.

