# Biome 6 — Seagrass Meadow | Hardware Specification

## Overview

This ESP32 node is the **Wave and Tide System controller** for the saltwater seagrass biome. Its sole job is motion control — driving a belt-mounted Nema 23 stepper to vertically oscillate a water-filled PVC chamber, pumping water in and out of the biome to simulate wave and tidal rhythms.

> **Design constraint:** No mechanical devices, metal, or electronics are permitted inside the glass habitat. All motion is generated externally.

---

## Electrical Hardware

| Component | Model / Spec | Notes |
|---|---|---|
| Microcontroller | ESP32-DevKitC-VIE | Main logic; manages timing and motion profiles |
| Stepper Motor | Nema 23 | High-torque, 3 Nm |
| Motor Driver | DM542 | Microstepping: **1600 pulse/rev**; Peak current: **4.2 A** |
| Feedback Sensor | Taiss Incremental Encoder | Optical AB 2-phase quadrature, **600 P/R**, 5–24 V, 6 mm shaft |
| Cooling Fan | 6015 60×60×15 mm | 12 V DC, 0.10A, dual ball bearing, 2-pin, always-on |
| PSU — Logic | Mean Well LRS-350-12 | 12 V / 29 A → buck converter → 5 V for ESP32 |
| PSU — Motor | Aclorol 36 V / 10 A | Direct to DM542 V+ |
| Buck Converter | Dorhea mini (4.5–24 V → 5 V, 3 A) | Steps 12 V down to 5 V for ESP32 and fans 12 V rail |

---

## Mechanical System

- **Drive:** Belt-driven stepper assembly; adjustable motor mount maintains a precise 90° belt angle
- **Linear Rail:** SFC16-1000 mm dual-rail slide
- **Belt:** 2GT, 15 mm width
- **Chamber:** 4" PVC pipe, 24" length; connected via **Fernco XL 3" flexible pipe coupler**
- **Motion:** Stepper drives rail vertically — chamber moves up/down, pumping water in and out of the seagrass meadow biome
- **Vent:** Opposite end of chamber is vented and returns to the system
- **Housings/Gears:** 3D-printed PETG (chemical resistance)

---

## DM542 DIP Switch Settings

| Switch | Position | Function |
|---|---|---|
| SW1 | OFF | Current setting |
| SW2 | OFF | Current setting |
| SW3 | OFF | Current setting |
| SW4 | ON | Standby current reduction (half current at idle) |
| SW5 | OFF | Microstep resolution |
| SW6 | OFF | Microstep resolution |
| SW7 | ON | Microstep resolution |
| SW8 | ON | Microstep resolution → **1600 pulse/rev** |

> **Note:** SW1/SW2/SW3 all OFF — verify peak current value against DM542 switch table. Spec sheet lists 4.2 A; confirm this matches the current setting before extended runs.

---

## Pin Assignments

| Signal | ESP32 GPIO | Direction | Notes |
|---|---|---|---|
| PUL+ (STEP) | GPIO25 | OUT | Pulse to DM542 — active high |
| DIR+ | GPIO26 | OUT | Direction to DM542 — active high |
| ENA+ | GPIO27 | OUT | Enable to DM542 — active high |
| ENA+ (Enable) | GPIO27 | OUT | Active-LOW in firmware — `LOW` = motor enabled, `HIGH` = motor free |
| ENC_A (White) | GPIO34 | IN | Quadrature channel A — input only, 10K pull-up to 3V3 |
| ENC_B (Green) | GPIO35 | IN | Quadrature channel B — input only, 10K pull-up to 3V3 |

---

## Wiring Diagram

```
════════════════════════════════════════════════════════
  POWER
════════════════════════════════════════════════════════

  Mean Well LRS-350-12 (12V / 29A)
  ├── 12V ──► Dorhea Buck IN+
  │           Dorhea Buck IN−  ──► GND rail
  │           Dorhea Buck OUT+ (5V) ──► ESP32 Pin 19 (5V0)
  │           Dorhea Buck OUT−      ──► ESP32 Pin 14 (GND)
  └── 12V jumped from Buck IN+ ──► Fan Red (12V)
                      GND rail ──► Fan Black (GND)

  Aclorol 36V / 10A
  ├── 36V ──► DM542 V+
  └── GND ──► DM542 GND

════════════════════════════════════════════════════════
  ESP32 → DM542  (Signal)
════════════════════════════════════════════════════════

  ESP32 GPIO25 (Pin 9L)  ──► DM542 PUL+  (STEP)
  ESP32 GPIO26 (Pin 10L) ──► DM542 DIR+
  ESP32 GPIO27 (Pin 11L) ──► DM542 ENA+

  ESP32 GND   (Pin 1R)   ──► DM542 PUL−
                              DM542 PUL− jumped ──► DIR−
                              DM542 DIR− jumped ──► ENA−

  (Common-cathode: all negative inputs share GND.
   Active-high 3.3V logic from ESP32.)

════════════════════════════════════════════════════════
  DM542 → Nema 23 Stepper Motor
════════════════════════════════════════════════════════

  DM542 A+ ◄── Blue  wire
  DM542 A− ◄── Red   wire
  DM542 B+ ◄── Green wire
  DM542 B− ◄── Black wire

════════════════════════════════════════════════════════
  ESP32 ← Taiss Encoder (600 P/R, 5V)
════════════════════════════════════════════════════════

  Encoder Red   ──► ESP32 Pin 19 (5V0)
  Encoder Black ──► ESP32 Pin 14 (GND)
  Encoder White ──► ESP32 GPIO34 (Pin 5L)  ← ENC_A
                         └── 10K resistor ──► ESP32 3V3 (Pin 1L)
  Encoder Green ──► ESP32 GPIO35 (Pin 6L)  ← ENC_B
                         └── 10K resistor ──► ESP32 3V3 (Pin 1L)
  Encoder Shield ── not connected

  (GPIO34/35 are input-only; no internal pull-ups.
   External 10K to 3V3 keeps signals within ESP32 logic levels
   despite encoder running at 5V.)
```

---

## Control Logic

- **Positioning:** Closed-loop feedback via the Taiss encoder. All physical limit switches have been removed.
- **Feedback resolution:** 600 P/R — ESP32 tracks exact chamber position, ensuring consistent stroke amplitude and preventing mechanical drift.

### Simulation Profiles

| Mode | Frequency | Amplitude | Purpose |
|---|---|---|---|
| Wave | High | Low | Surface agitation / oxygenation |
| Tide | Low | High | Expose or submerge biome zones |

---

## MQTT Integration

> **TODO — topics to be confirmed against the control network.**

| Topic | Direction | Payload |
|---|---|---|
| `biome/6/wave/setpoint` | Subscribe | Mode, frequency, amplitude params |
| `biome/6/wave/telemetry` | Publish | Current mode, encoder position, faults |

---

## Deployment Status

- Board: **in hand, active**
- Firmware: **running** — AccelStepper closed-loop wave simulation, no MQTT yet (standalone)
- Mechanical assembly: complete per spec above
- MQTT: not yet implemented — current firmware is fully local/offline

---

## Planned Features (Future R&D)

- **Tide Chart Sync:** Pull real-time tide data via Wi-Fi API; sync biome to a specific coastal location
- **Weather Integration:** Adjust wave intensity based on local or simulated weather (storm surges, etc.)
- **Motor Upgrade:** ClearPath MCVC by Teknic (integrated brushless servo — lower noise, higher precision)
- **Atmospheric Linking:** Synchronize with the miniBIOTA Rain System for cohesive seasonal cycles
