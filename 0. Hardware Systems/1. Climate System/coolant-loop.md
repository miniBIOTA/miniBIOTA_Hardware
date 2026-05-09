# Coolant Loop

## Current Architecture

- The Climate System uses a shared chilled coolant loop.
- Coolant is a water/glycol mixture.
- The current loop serves the four atmospheric heat exchangers on Biomes 2-5.
- Each heat exchanger branch has its own 12 V circulation pump.
- Cooling is actively controlled by each biome's ESP32 rather than running as constant flow by default.

## Cooling Source

- Cooling source: laboratory chiller.
- Chiller capability: approximately -30 C.
- Previously used working coolant temperature: approximately 0 C.
- Current status: chiller under repair.

The detailed chiller-side plumbing is not yet documented.

## Branch Pattern

Each current atmosphere branch follows this pattern:

```text
Shared chilled loop
  -> branch pump
  -> atmospheric heat exchanger inlet
  -> switchback path across rear glass
  -> exchanger outlet
  -> return to shared loop
```

Each branch is monitored by a DS18B20 probe installed inside the heat exchanger.

## Known Open Details

- Exact chiller model/spec.
- Exact manifold layout.
- Exact glycol ratio.
- Exact PEX routing and fitting sizes.
- Branch isolation valves, if any.
- Future fusing, disconnects, and service shutoffs for pump/controller wiring.

