# Climate Pumps And Control

## Current Pump Hardware

Each current atmosphere heat exchanger branch uses:

- Pump: BYT-7A015 DC 12 V solar hot water heater circulation pump.
- Rated flow: 8 LPM / 2.1 GPM.
- Max head: 3 m / 9.8 ft.
- Driver: DC 5-36 V 15 A, max 30 A, 400 W dual high-power MOSFET trigger switch drive module, 0-20 kHz PWM.

Each Biome 2-5 controller has its own pump and MOSFET module.

## Power Pattern

- One shared Mean Well LRS-350-12 power supply provides the 12 V rail for the four sensor/controller systems.
- Each biome taps the 12 V rail.
- At each biome, the 12 V tap feeds:
  - Dorhea buck converter input for ESP32 5 V power.
  - MOSFET module power input for pump switching.
- ESP32 GPIO27 drives the MOSFET PWM/control input.
- MOSFET control-side GND is tied to the buck converter output GND and ESP32 GND.

## Control Model

- The ESP32 owns local pump control.
- The DS18B20 reports coolant temperature inside the heat exchanger.
- Firmware maps temperature relative to the current target window into pump PWM.
- Higher-level software publishes temperature setpoints; it does not directly command pump ON/OFF in the normal control model.

## Safety Boundary

Changing pump switching, PWM behavior, thermostat logic, hysteresis, or setpoint parsing is a live-biosphere control change and requires explicit approval.

