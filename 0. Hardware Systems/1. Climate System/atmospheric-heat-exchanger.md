# Atmospheric Heat Exchanger Spec

**Project:** MiniBIOTA
**Component name:** Atmospheric Heat Exchanger
**Current deployment:** Four atmosphere tanks, one each for Biomes 2-5
**Purpose:** External cooling panel for condensation, humidity control, and rain-cycle support

## 1. Overview

The Atmospheric Heat Exchanger is a custom-built PVC cooling panel mounted to the outside back wall of each MiniBIOTA atmosphere tank. Its purpose is to circulate chilled coolant across the back glass of the vertical atmosphere tank, cooling the inner glass surface and encouraging condensation from humid internal air.

That condensation forms on the inside surface of the atmosphere glass, then runs downward into the cloud/rain collection system. This allows the atmosphere tank to act as a cooling and water-cycle chamber without placing active mechanical equipment inside the biosphere.

The current system uses four atmospheric heat exchangers, one for each existing atmosphere tank on Biomes 2-5. Additional heat exchangers may be built in the future for other biome or atmosphere applications, although those future versions may differ in design.

The exchanger belongs to the Climate System. The cloud reservoirs and rainfall distribution belong to the Rain System.

## 2. Main Dimensions

The heat exchanger is built from sheet PVC.

**Base panel dimensions:**

- Height: 54 cm
- Width: 41 cm
- Orientation: portrait
- PVC thickness: 1.2 cm

When mounted, the 54 cm side runs vertically, and the 41 cm side runs horizontally.

## 3. Material

The structural body of the heat exchanger is made entirely from 1.2 cm thick sheet PVC.

This includes:

- Main back plate
- Perimeter lip/spacer
- Internal switchback ribs
- Threaded PVC fitting areas

The PVC-to-PVC joints are bonded with standard PVC cement. The PVC-to-glass attachment is made with aquarium-safe silicone.

## 4. Cavity Construction

A 1.2 cm by 1.2 cm PVC lip is attached around the full perimeter of the cut PVC sheet. This perimeter lip serves as a spacer and creates the internal water cavity.

Because the atmosphere tank glass acts as the front wall of the heat exchanger, the internal coolant chamber is formed by:

- The PVC back plate
- The 1.2 cm perimeter spacer
- The internal ribs
- The exterior surface of the atmosphere tank glass

There is no separate PVC front cover sheet. The glass itself completes the water chamber.

The internal cavity depth is approximately 1.2 cm.

## 5. Glass Interface

The heat exchanger is mounted to the outside back wall of the vertical atmosphere tank. The atmosphere tank glass is approximately 1/4 inch thick.

Chilled coolant flows directly against the outside surface of the glass. The opposite side of that same glass is exposed to the humid air inside the sealed atmosphere tank.

This means the cooling effect must pass through the 1/4 inch glass before reaching the internal atmosphere. The glass thickness reduces thermal efficiency somewhat, but the design still functions by chilling the inner glass surface enough to trigger condensation.

## 6. Silicone Sealing

Aquarium silicone is applied between the PVC exchanger and the glass.

The silicone bead runs:

- Around the full perimeter lip
- Along the internal ribs

The internal ribs are sealed to the glass, which forces the coolant to follow the intended switchback flow path rather than bypassing the channels.

The heat exchanger has been pressure tested and leak tested while assembled, and it has successfully operated without known leaks.

## 7. Internal Rib Layout

Inside the cavity are six internal PVC ribs.

Each rib is made from the same 1.2 cm thick sheet PVC material and is approximately:

- Cross section: 1.2 cm by 1.2 cm
- Length: roughly 31 cm
- Quantity: 6 ribs

The ribs run horizontally across the width of the heat exchanger. They are evenly spaced from bottom to top.

Because the exchanger is 41 cm wide and each rib is about 31 cm long, each rib leaves an open side gap of roughly 7 to 8 cm. These gaps alternate left and right, creating a switchback path for the coolant.

Approximate vertical spacing can be treated as evenly distributed across the 54 cm panel height. The exact spacing cannot be measured now because the units are already assembled and mounted, but the ribs were cut and placed evenly during construction.

## 8. Flow Path

When looking at the heat exchanger from the back:

1. Coolant enters at the bottom-left.
2. It flows horizontally across the bottom channel toward the right side.
3. It turns upward through the open gap.
4. It flows back left through the next channel.
5. It continues alternating left and right as it rises.
6. It exits at the top-right.

The six ribs create a snaking internal flow path that forces the coolant to travel across much of the glass contact area before exiting.

The inlet and outlet are placed diagonally from each other, which helps maximize the travel distance through the exchanger.

## 9. Plumbing And Fittings

The exchanger connects to the cooling loop using 1/2 inch PEX.

The inlet and outlet use bronze 90-degree fittings that connect the PEX tubing to the heat exchanger.

The fitting arrangement is approximately:

- 1/2 inch PEX connection
- Bronze 90-degree fitting
- Approximately 1/2 inch internal threading
- PVC female threaded receiver
- Approximately 3/4 inch external thread into the sheet PVC

The exact fitting sizes should be verified in future documentation, but the working system uses 1/2 inch PEX plumbing with threaded PVC connections into the exchanger body.

## 10. Temperature Probe Port

A third fitting is located near the center of the heat exchanger.

This fitting holds a Hilitchi DS18B20 waterproof digital temperature probe that measures the coolant temperature inside the exchanger. The probe is installed into a drilled PVC plug or cap, then potted permanently into that cap.

The probe assembly is permanent within the plug, but the plug itself can be unscrewed and replaced if needed.

The temperature probe is connected to the matching biome ESP32 controller.

## 11. Coolant

The exchanger currently circulates a water and glycol mixture.

The exact glycol ratio has not been finalized. The system is currently not running while the chiller is being repaired, but when operating, the coolant loop was reaching approximately:

- Current working coolant temperature: 0 C
- Lab chiller capability: down to approximately -30 C

The system has not been operated at the full low-temperature capability.

## 12. Pump And Flow

Each exchanger loop is driven by a BYT-7A015 12 V circulation pump rated at approximately:

- 8 liters per minute
- 2.1 gallons per minute
- Max head: 3 meters
- Max head: 9.8 feet

Because the loop is sealed and continuous, the pump is not lifting water in an open system. Although the pump pushes coolant upward through part of the loop, the returning coolant on the opposite side helps balance the system. This reduces the effective load compared with pumping against gravity in an open loop.

## 13. Cooling Source And Control

The atmospheric heat exchanger is connected to a lab chiller system. The detailed chiller-side plumbing is outside the scope of this spec.

The temperature probe inside the exchanger reports coolant temperature to an ESP32 controller. The controller uses that temperature reading to decide when to turn the exchanger pump on or off.

The purpose of this control is to regulate how much cooling reaches the atmosphere tank.

## 14. Condensation And Rain Function

The atmospheric heat exchanger cools the back glass of the atmosphere tank. Humid air inside the sealed atmosphere contacts the chilled glass surface, causing water vapor to condense.

The condensation forms on the inside surface of the glass, opposite the heat exchanger, then runs downward into the atmosphere's cloud/rain system.

This supports MiniBIOTA's water-cycle function by helping convert humid air back into liquid water without placing pumps, radiators, fans, or mechanical cooling equipment inside the living biosphere.

## 15. Leak Behavior And Biosphere Safety

The heat exchanger is mounted externally. The glycol-water coolant is outside the living biosphere and flows against the exterior surface of the atmosphere glass.

If the exchanger or plumbing were to leak, the leak would occur outside the biosphere rather than directly into the enclosed habitat. This helps protect the organisms and internal chemistry from coolant contamination.

The glass wall separates the coolant loop from the internal atmosphere.

## 16. Serviceability

The atmospheric heat exchanger is effectively permanent once mounted, but it can be removed if necessary.

Removal would be destructive. To replace a failed exchanger, the existing unit would need to be cut off or broken apart, then the remaining silicone and adhesive material would need to be cleaned from the glass before a new exchanger could be built and attached.

The temperature probe plug is more serviceable than the exchanger body itself because it can be unscrewed and replaced.

## 17. Current Status

The current atmospheric heat exchanger design has been built, mounted, pressure tested, leak tested, and operated successfully.

No major problems have been observed so far. Known considerations include:

- Thermal transfer must pass through 1/4 inch glass
- The exchanger is destructive to remove
- The glycol ratio is not yet finalized
- The chiller is currently under repair
- Future heat exchangers may need design adjustments depending on biome-specific requirements

## 18. Future Expansion Note

The current spec applies to the existing four atmospheric heat exchangers used on the current MiniBIOTA atmosphere tanks.

Future plans may include additional heat exchangers for all six biomes and potentially new atmosphere tanks for the lake biome and seagrass meadow biome. Those future units may be designed separately and may differ from this current atmospheric heat exchanger design.

## Open Items

- Verify exact fitting thread sizes.
- Finalize glycol ratio.
- Document chiller-side plumbing.
- Document any future exchanger variants for Biomes 1 or 6 separately.
