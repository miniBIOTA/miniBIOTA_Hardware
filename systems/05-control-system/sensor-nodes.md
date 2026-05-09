# Sensor Nodes

## Current Deployed Pattern

Biomes 2-5 share the same controller architecture:

- ESP32-DevKitC-VIE / ESP-WROOM-32 DevKitC.
- ESP32 screw-terminal breakout board.
- Two GY-SHT31-D temperature/humidity sensors:
  - One in the biome.
  - One in the atmosphere.
- Two Hosyond 0.96 in SSD1306 OLED displays:
  - One for biome readings.
  - One for atmosphere readings and pump percentage.
- One Hilitchi DS18B20 probe measuring coolant inside the atmospheric heat exchanger.
- One BYT-7A015 12 V pump.
- One PWM MOSFET module controlled from GPIO27.
- One Dorhea buck converter stepping 12 V down to 5 V for the ESP32.
- One 2x6 terminal block distribution module for 3V3/GND sensor power.

## Pin Assignments

| Signal | ESP32 GPIO | Notes |
|---|---:|---|
| I2C Bus 1 SDA | GPIO21 | Atmosphere SHT31-D + atmosphere OLED |
| I2C Bus 1 SCL | GPIO22 | Atmosphere SHT31-D + atmosphere OLED |
| I2C Bus 2 SDA | GPIO18 | Biome SHT31-D + biome OLED |
| I2C Bus 2 SCL | GPIO19 | Biome SHT31-D + biome OLED |
| DS18B20 data | GPIO4 | 4.7k pull-up to ESP32 3V3 |
| Pump PWM | GPIO27 | PWM/control input to MOSFET module |

## I2C Devices

- SHT31-D address: `0x44`.
- OLED address: `0x3C`.
- I2C speed: 100 kHz for long-cable stability.

## Current Known Issues

- SDA/SCL should be rewired so they are not paired together in a twisted pair.
- Some SHT31-D modules may be damaged by water exposure.
- Connection quality is not yet stable across all Biomes 2-5.
- Connector standard remains open.
- Wire color standard remains open.
- Branch fusing/disconnect plan remains open.

## Per-Biome Installed Specs

Use the biome folder for exact installed-instance detail:

- `../../2. Lakeshore Biome/biome_hardware.md`
- `../../3. Lowland Meadow Biome/biome_hardware.md`
- `../../4. Mangrove Forest Biome/biome_hardware.md`
- `../../5. Marine Shore Biome/biome_hardware.md`
