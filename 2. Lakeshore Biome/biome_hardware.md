# Biome 2 - Lakeshore | Hardware Specification

## Overview

This ESP32 node is the sensor and cooling-pump controller for the Lakeshore biome. It reads one temperature/humidity sensor in the biome, one temperature/humidity sensor in the atmosphere, one coolant temperature probe in the heat exchanger, displays local readings on two OLED screens, and controls one 12 V coolant circulation pump through a PWM MOSFET module.

The four sensor biomes, Biomes 2-5, are wired with the same controller architecture unless a per-biome status note says otherwise.

---

## Electrical Hardware

| Component | Model / Spec | Quantity | Notes |
|---|---|---:|---|
| Microcontroller | ESP32-DevKitC-VIE / ESP-WROOM-32 DevKitC | 1 | Main logic, WiFi, OTA, MQTT, local thermostat loop |
| ESP32 breakout | ESP32 Breakout Board 3.5 mm / 0.14 in Terminal GPIO Expansion Board for 0.9 in / 1.0 in ESP32 Module ESP-WROOM-32 ESP32-DevKitC | 1 | Screw-terminal GPIO expansion board |
| Biome temperature/humidity sensor | GY-SHT31-D SHT31-D temperature and humidity sensor module, I2C, 2.4-5.5 V | 1 | Mounted in biome airspace |
| Atmosphere temperature/humidity sensor | GY-SHT31-D SHT31-D temperature and humidity sensor module, I2C, 2.4-5.5 V | 1 | Mounted in atmosphere airspace |
| Biome OLED display | Hosyond 0.96 in OLED I2C/IIC display, 128x64, SSD1306, blue | 1 | Displays biome sensor readings |
| Atmosphere OLED display | Hosyond 0.96 in OLED I2C/IIC display, 128x64, SSD1306, blue | 1 | Displays atmosphere sensor readings and pump percentage |
| Coolant probe | Hilitchi DS18B20 waterproof digital temperature probe | 1 | Measures coolant temperature inside the heat exchanger |
| DS18B20 pull-up | 4.7k resistor | 1 | Pulls DS18B20 data line to ESP32 3V3 |
| Coolant pump | BYT-7A015 DC 12 V solar hot water heater circulation pump, 3 m head, 8 LPM / 2.1 GPM | 1 | One pump per biome cooling branch |
| Pump driver | DC 5-36 V 15 A, max 30 A, 400 W dual high-power MOSFET trigger switch drive module, 0-20 kHz PWM | 1 | Used as a single PWM-controlled pump switch; dual MOSFET package is for higher current capacity |
| Buck converter | Dorhea mini adjustable buck converter, DC 4.5-24 V input to 5 V 3 A output | 1 | Steps the 12 V rail down to 5 V for the ESP32 |
| Power distribution module | 2x6 position terminal block distribution module, 2P screw terminal to 2.54 mm Dupont header | 1 | Distributes ESP32 3V3 and GND to sensors, OLEDs, and probe pull-up |
| Shared 12 V supply | Mean Well LRS-350-12, 12 V / 29 A, 350 W | Shared | Powers all four sensor-biome controller systems and pumps |

---

## Power Architecture

- One shared Mean Well LRS-350-12 provides a 12 V rail that runs across the four sensor-biome controllers.
- Each biome controller taps the shared 12 V rail.
- At each biome controller, the 12 V tap feeds:
  - Dorhea buck converter input.
  - MOSFET module power input for the 12 V pump.
- The Dorhea buck converter outputs 5 V to the ESP32 5V/VIN input.
- The MOSFET module output powers and PWM-controls the BYT-7A015 pump.
- The MOSFET control-side GND is tied to the negative output side of the buck converter, sharing ground with the ESP32.
- Sensors, OLEDs, and the DS18B20 pull-up are powered from ESP32 3V3 and GND through the 2x6 terminal block distribution module.

> Future add-on: no fuse, inline switch, emergency disconnect, or branch protection is currently documented between the Mean Well supply and the controller taps. Add these during a future electrical safety pass.

---

## Pin Assignments

| Signal | ESP32 GPIO | Direction | Notes |
|---|---:|---|---|
| I2C Bus 1 SDA | GPIO21 | I/O | Atmosphere SHT31-D + atmosphere OLED |
| I2C Bus 1 SCL | GPIO22 | I/O | Atmosphere SHT31-D + atmosphere OLED |
| I2C Bus 2 SDA | GPIO18 | I/O | Biome SHT31-D + biome OLED |
| I2C Bus 2 SCL | GPIO19 | I/O | Biome SHT31-D + biome OLED |
| DS18B20 data | GPIO4 | IN | 4.7k pull-up to ESP32 3V3 |
| Pump PWM | GPIO27 | OUT | PWM/control input to MOSFET module |

### I2C Devices

| Bus | Devices | Address / Setting |
|---|---|---|
| I2C Bus 1 | Atmosphere SHT31-D, atmosphere OLED | SHT31 `0x44`, OLED `0x3C` |
| I2C Bus 2 | Biome SHT31-D, biome OLED | SHT31 `0x44`, OLED `0x3C` |

- I2C speed in firmware: 100 kHz for long-cable stability.
- The current wiring needs to be reworked so SDA and SCL are not paired together in a twisted pair; that pairing is suspected to be contributing to signal quality problems.

---

## Wiring Diagram

```text
POWER

Mean Well LRS-350-12 shared 12 V rail
  -> Biome 2 12 V tap
       -> Dorhea buck IN+
       -> MOSFET DC+

Mean Well GND rail
  -> Biome 2 GND tap
       -> Dorhea buck IN-
       -> MOSFET DC-

Dorhea buck OUT+ (5 V)
  -> ESP32 5V/VIN

Dorhea buck OUT- (GND)
  -> ESP32 GND
  -> MOSFET control GND

MOSFET OUT+/OUT-
  -> BYT-7A015 pump +/-

ESP32 GPIO27
  -> MOSFET PWM/control +
```

```text
LOW-VOLTAGE SENSOR POWER

ESP32 3V3, pin 1
  -> 2x6 terminal distribution module +
       -> atmosphere SHT31 VCC
       -> biome SHT31 VCC
       -> atmosphere OLED VCC
       -> biome OLED VCC
       -> DS18B20 4.7k data pull-up

ESP32 GND, pin 1
  -> 2x6 terminal distribution module -
       -> atmosphere SHT31 GND
       -> biome SHT31 GND
       -> atmosphere OLED GND
       -> biome OLED GND
       -> DS18B20 GND
```

---

## Control Logic

- The ESP32 reads biome and atmosphere SHT31-D sensors, the DS18B20 coolant probe, and publishes telemetry over MQTT.
- The ESP32 owns local pump control.
- Pump output is proportional PWM based on the liquid/coolant temperature target window in firmware.
- Setpoints are received through MQTT, but direct pump switching remains local to the ESP32.

Changing pump switching, thermostat logic, setpoint handling, telemetry serialization, WiFi/MQTT behavior, or OTA behavior is a live-biosphere control change and requires explicit approval.

---

## System References

- Control System sensor node architecture: `../systems/05-control-system/sensor-nodes.md`
- Climate System pump/control architecture: `../systems/01-climate-system/pumps-and-control.md`
- Atmospheric heat exchanger data sheet: `../systems/01-climate-system/atmospheric-heat-exchanger.md`

---

## Current Observed Status - 2026-05-09

- Atmosphere SHT31-D shows `Sensor Err` on the local OLED.
- Biome SHT31-D shows readings.
- Biome OLED display is dim, suggesting possible signal quality or connection quality issues, though the display still works.
- Root causes are not fully isolated. Current suspects include SDA/SCL twisted-pair wiring, general connection quality, and possible water-damaged SHT31 modules.
- Rewire and sensor replacement pass is pending.

---

## Open Items

- Connector plan is still open; XT30/JST-XH may be used, but the final connector standard has not been selected.
- Wire color standard is not established yet.
- Add branch fusing, switching, or emergency disconnects in a future safety pass.
- Update this file after the rewire and sensor replacement pass.
