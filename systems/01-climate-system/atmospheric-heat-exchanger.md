# Atmospheric Heat Exchanger

## Overview

The Atmospheric Heat Exchanger is a custom PVC cooling panel mounted to the outside back wall of each current miniBIOTA atmosphere tank. Chilled coolant flows across the exterior surface of the atmosphere glass, cooling the inner glass surface and encouraging condensation from humid internal air.

The condensation forms on the inside glass surface, then runs downward into the cloud/rain collection system. This supports the water cycle without placing active mechanical cooling hardware inside the living biosphere.

## Current Deployment

- Quantity: 4.
- Location: one on each existing atmosphere tank for Biomes 2-5.
- Current status: built, mounted, pressure tested, leak tested, and previously operated successfully.
- Chiller status: chiller is currently under repair.

## Main Dimensions

| Feature | Spec |
|---|---|
| Base panel height | 54 cm |
| Base panel width | 41 cm |
| Orientation | Portrait; 54 cm side vertical, 41 cm side horizontal |
| PVC thickness | 1.2 cm |
| Internal cavity depth | Approximately 1.2 cm |
| Atmosphere glass thickness | Approximately 1/4 in |

## Materials And Construction

- Structural body is made from 1.2 cm thick sheet PVC.
- PVC components include the main back plate, perimeter lip/spacer, internal switchback ribs, and threaded fitting areas.
- PVC-to-PVC joints are bonded with standard PVC cement.
- PVC-to-glass attachment uses aquarium-safe silicone.
- There is no separate PVC front cover sheet; the atmosphere tank glass completes the coolant chamber.

## Cavity And Glass Interface

The internal coolant chamber is formed by:

- PVC back plate.
- 1.2 cm perimeter spacer.
- Internal ribs.
- Exterior surface of the atmosphere tank glass.

Coolant flows directly against the outside surface of the glass. The opposite side of that glass is exposed to humid air inside the atmosphere tank. Thermal transfer must pass through the 1/4 in glass, reducing efficiency somewhat, but the design has worked well enough to trigger condensation.

## Silicone Sealing

Aquarium silicone is applied:

- Around the full perimeter lip.
- Along the internal ribs.

The rib seals force coolant through the intended switchback path rather than allowing it to bypass the channels.

## Internal Rib Layout

| Feature | Spec |
|---|---|
| Rib quantity | 6 |
| Rib material | 1.2 cm sheet PVC |
| Rib cross section | Approximately 1.2 cm x 1.2 cm |
| Rib length | Roughly 31 cm |
| Orientation | Horizontal across the exchanger width |
| Side gaps | Approximately 7-8 cm, alternating left and right |

The ribs are evenly distributed from bottom to top. Exact spacing is not currently measurable because the units are assembled and mounted.

## Flow Path

Viewed from the back:

1. Coolant enters at bottom-left.
2. It flows horizontally across the bottom channel toward the right.
3. It turns upward through the open side gap.
4. It flows back left through the next channel.
5. It alternates left and right through the switchback path.
6. It exits at top-right.

The diagonal inlet/outlet placement maximizes travel distance across the glass contact area.

## Plumbing And Fittings

- Loop plumbing uses 1/2 in PEX.
- Inlet and outlet use bronze 90-degree fittings.
- Working arrangement is approximately:
  - 1/2 in PEX connection.
  - Bronze 90-degree fitting.
  - Approximately 1/2 in internal threading.
  - PVC female threaded receiver.
  - Approximately 3/4 in external thread into the sheet PVC.

Exact fitting thread sizes still need verification.

## Temperature Probe Port

A third fitting near the center of the heat exchanger holds the coolant temperature probe.

- Probe: Hilitchi DS18B20 waterproof digital temperature probe.
- The probe is installed into a drilled PVC plug or cap.
- The probe is potted permanently into that plug/cap.
- The plug can be unscrewed and replaced if needed.
- The probe connects to the matching biome ESP32 controller.

## Coolant

- Current coolant: water and glycol mixture.
- Exact glycol ratio: not finalized.
- Previous working coolant temperature: approximately 0 C.
- Lab chiller capability: approximately -30 C.
- The system has not been operated at the full low-temperature capability.

## Pump And Flow

Each exchanger branch is driven by a BYT-7A015 12 V circulation pump:

- Flow rating: 8 LPM / 2.1 GPM.
- Max head: 3 m / 9.8 ft.

Because the loop is sealed and continuous, the pump is not lifting water in an open system. Returning coolant helps balance the upward push, reducing effective load compared with open vertical pumping.

## Condensation And Rain Function

The exchanger cools the rear glass of the atmosphere tank. Humid internal air contacts the chilled inner glass surface, causing water vapor to condense. Condensate runs downward into the atmosphere's cloud/rain system.

The exchanger belongs to the Climate System. The cloud reservoirs and rainfall distribution belong to the Rain System.

## Leak Behavior And Biosphere Safety

The exchanger is mounted externally. Glycol-water coolant stays outside the living biosphere and flows against the exterior surface of the atmosphere glass.

If the exchanger or plumbing leaks, the leak should occur outside the biosphere rather than directly into the habitat. The glass wall separates coolant from the internal atmosphere.

## Serviceability

The exchanger body is effectively permanent once mounted. Removal would be destructive: the existing unit would need to be cut off or broken apart, and remaining silicone/adhesive would need to be cleaned from the glass before replacement.

The temperature probe plug is more serviceable because it can be unscrewed and replaced.

## Open Items

- Verify exact fitting thread sizes.
- Finalize glycol ratio.
- Document chiller-side plumbing.
- Document any future exchanger variants for Biomes 1 or 6 separately.

