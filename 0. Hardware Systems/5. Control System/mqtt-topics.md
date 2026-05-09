# MQTT Topics

## Sensor Node Topics

| Topic | Direction | Payload |
|---|---|---|
| `miniBIOTA/biome/<id>/status` | ESP32 -> Wyse/App | `"online"` on boot |
| `miniBIOTA/biome/<id>/telemetry` | ESP32 -> Wyse/App | JSON telemetry every 10 seconds where sensors exist |
| `miniBIOTA/biome/<id>/setpoint` | Wyse/App -> ESP32 | Float target temperature string, for example `"22.5"` |

## Telemetry Payload For Biomes 2-5

```json
{
  "atmo_t": 24.50,
  "atmo_h": 65.2,
  "bio_t": 26.80,
  "bio_h": 70.1,
  "liq_t": 18.50,
  "pump_pct": 35,
  "target_t": 0.0
}
```

Missing sensor values must serialize as JSON `null`, never `nan`.

## Live-Control Boundary

Publishing to `miniBIOTA/biome/<id>/setpoint` changes live control behavior and requires explicit approval.

Direct pump ON/OFF commands are not the normal control model. The ESP32 owns local pump control from setpoints and sensor readings.

