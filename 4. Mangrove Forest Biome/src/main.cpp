#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoOTA.h>
#include <PubSubClient.h>
#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>
#include <Adafruit_SHT31.h>
#include <OneWire.h>
#include <DallasTemperature.h>

// ---------------------------
// Network
// ---------------------------
const char* WIFI_SSID    = "mB2.4";
const char* WIFI_PASS    = "qYKEQe8R763HKmk";
const char* OTA_HOSTNAME = "biome4-mangrove";
const char* MQTT_BROKER  = "192.168.8.228";
const int   MQTT_PORT    = 1883;
const char* MQTT_CLIENT  = "biome4-mangrove";

const char* TOPIC_TELEMETRY = "miniBIOTA/biome/4/telemetry";
const char* TOPIC_STATUS    = "miniBIOTA/biome/4/status";
const char* TOPIC_SETPOINT  = "miniBIOTA/biome/4/setpoint";

// ---------------------------
// Pins
// ---------------------------
#define SDA_1         21
#define SCL_1         22
#define SDA_2         18
#define SCL_2         19
#define ONE_WIRE_BUS   4
#define PUMP_PIN      27
#define I2C_SPEED     100000

// ---------------------------
// Pump config
// ---------------------------
float TARGET_TEMP_C    = 0.0;
float MAX_TEMP_C       = 5.0;
const int MIN_PUMP_PWM = 40;
const int MAX_PUMP_PWM = 255;
const int KICKSTART_MS = 250;

// ---------------------------
// I2C / sensors / displays
// ---------------------------
#define SCREEN_WIDTH  128
#define SCREEN_HEIGHT  64

TwoWire I2C_1 = TwoWire(0);
TwoWire I2C_2 = TwoWire(1);

Adafruit_SSD1306 displayAtmosphere(SCREEN_WIDTH, SCREEN_HEIGHT, &I2C_1, -1);
Adafruit_SSD1306 displayBiome(SCREEN_WIDTH, SCREEN_HEIGHT, &I2C_2, -1);

Adafruit_SHT31 shtAtmosphere(&I2C_1);
Adafruit_SHT31 shtBiome(&I2C_2);

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature sensors(&oneWire);

// ---------------------------
// State
// ---------------------------
bool pumpWasOff  = true;
int  pumpPWM     = 0;
int  pumpPercent = 0;

unsigned long lastUpdate      = 0;
unsigned long lastTelemetryMs = 0;
const long UPDATE_INTERVAL    = 2000;
const long TELEMETRY_MS       = 10000;

// ---------------------------
// MQTT
// ---------------------------
WiFiClient   wifiClient;
PubSubClient mqtt(wifiClient);

void mqttCallback(char* topic, byte* payload, unsigned int length) {
  if (strcmp(topic, TOPIC_SETPOINT) == 0) {
    char buf[16];
    unsigned int len = min(length, (unsigned int)15);
    memcpy(buf, payload, len);
    buf[len] = '\0';
    float target = atof(buf);
    if (target > -20.0 && target < 50.0) {
      TARGET_TEMP_C = target;
      MAX_TEMP_C    = target + 5.0;
      Serial.printf("Setpoint updated: target=%.1f max=%.1f\n", TARGET_TEMP_C, MAX_TEMP_C);
    }
  }
}

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqtt.connect(MQTT_CLIENT)) {
      Serial.println("connected.");
      mqtt.publish(TOPIC_STATUS, "online");
      mqtt.subscribe(TOPIC_SETPOINT);
    } else {
      Serial.printf("failed rc=%d, retrying in 5s\n", mqtt.state());
      delay(5000);
    }
  }
}

// ---------------------------
// Setup
// ---------------------------
void setup() {
  Serial.begin(115200);

  I2C_1.begin(SDA_1, SCL_1, I2C_SPEED);
  I2C_2.begin(SDA_2, SCL_2, I2C_SPEED);

  pinMode(PUMP_PIN, OUTPUT);
  analogWrite(PUMP_PIN, 0);

  if (!displayAtmosphere.begin(SSD1306_SWITCHCAPVCC, 0x3C)) Serial.println("Disp 1 Fail");
  if (!displayBiome.begin(SSD1306_SWITCHCAPVCC, 0x3C))      Serial.println("Disp 2 Fail");

  displayAtmosphere.clearDisplay();
  displayBiome.clearDisplay();
  displayAtmosphere.drawLine(0, 8, 128, 8, SSD1306_WHITE);
  displayBiome.drawLine(0, 8, 128, 8, SSD1306_WHITE);
  displayAtmosphere.display();
  displayBiome.display();

  shtAtmosphere.begin(0x44);
  shtBiome.begin(0x44);
  sensors.begin();

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);
  Serial.print("Connecting to WiFi");
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println();
  Serial.print("Connected. IP: ");
  Serial.println(WiFi.localIP());

  ArduinoOTA.setHostname(OTA_HOSTNAME);
  ArduinoOTA.onStart([]() { Serial.println("OTA start"); });
  ArduinoOTA.onEnd([]()   { Serial.println("OTA done");  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("OTA error [%u]\n", error);
  });
  ArduinoOTA.begin();
  Serial.println("OTA ready.");

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  mqtt.setCallback(mqttCallback);
  connectMQTT();

  Serial.println("Setup complete.");
}

// ---------------------------
// Loop
// ---------------------------
void loop() {
  ArduinoOTA.handle();
  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();

  unsigned long now = millis();

  if (now - lastUpdate >= UPDATE_INTERVAL) {
    lastUpdate = now;

    float atmoTempC  = shtAtmosphere.readTemperature();
    float atmoHum    = shtAtmosphere.readHumidity();
    float biomeTempC = shtBiome.readTemperature();
    float biomeHum   = shtBiome.readHumidity();
    sensors.requestTemperatures();
    float liquidTempC = sensors.getTempCByIndex(0);

    float atmoTempF   = (atmoTempC * 1.8) + 32.0;
    float biomeTempF  = (biomeTempC * 1.8) + 32.0;
    float liquidTempF = (liquidTempC * 1.8) + 32.0;

    pumpPWM = 0;
    if (liquidTempC > -100) {
      if (liquidTempC <= TARGET_TEMP_C) {
        pumpPWM = 0;
      } else if (liquidTempC >= MAX_TEMP_C) {
        pumpPWM = MAX_PUMP_PWM;
      } else {
        float frac = (liquidTempC - TARGET_TEMP_C) / (MAX_TEMP_C - TARGET_TEMP_C);
        pumpPWM = MIN_PUMP_PWM + (int)(frac * (MAX_PUMP_PWM - MIN_PUMP_PWM));
      }

      if (pumpPWM > 0) {
        if (pumpWasOff) {
          analogWrite(PUMP_PIN, 255);
          delay(KICKSTART_MS);
          pumpWasOff = false;
        }
        analogWrite(PUMP_PIN, pumpPWM);
      } else {
        analogWrite(PUMP_PIN, 0);
        pumpWasOff = true;
      }
      pumpPercent = map(pumpPWM, 0, 255, 0, 100);
    }

    // Atmosphere display
    displayAtmosphere.setTextColor(SSD1306_WHITE, SSD1306_BLACK);
    displayAtmosphere.setTextSize(1);
    displayAtmosphere.setCursor(0, 0);
    displayAtmosphere.print(F("ATMO | Pump: "));
    if (pumpPercent > 0) {
      displayAtmosphere.print(pumpPercent);
      displayAtmosphere.print(F("%   "));
    } else {
      displayAtmosphere.print(F("OFF  "));
    }
    displayAtmosphere.setCursor(0, 12);
    if (!isnan(atmoTempC)) {
      displayAtmosphere.setTextSize(2);
      displayAtmosphere.print(atmoTempC, 1);
      displayAtmosphere.setTextSize(1);
      displayAtmosphere.print(F("C "));
      displayAtmosphere.setTextSize(2);
      displayAtmosphere.print(atmoTempF, 1);
      displayAtmosphere.setTextSize(1);
      displayAtmosphere.print(F("F "));
    } else {
      displayAtmosphere.print(F("SENSOR ERR   "));
    }
    displayAtmosphere.setCursor(0, 32);
    displayAtmosphere.setTextSize(2);
    displayAtmosphere.print(F("RH: "));
    if (!isnan(atmoHum)) {
      displayAtmosphere.print(atmoHum, 1);
      displayAtmosphere.setTextSize(1);
      displayAtmosphere.print(F("%  "));
    }
    displayAtmosphere.setCursor(0, 54);
    displayAtmosphere.setTextSize(1);
    displayAtmosphere.print(F("Liq: "));
    if (liquidTempC > -127) {
      displayAtmosphere.print(liquidTempC, 1);
      displayAtmosphere.print(F("C / "));
      displayAtmosphere.print(liquidTempF, 0);
      displayAtmosphere.print(F("F    "));
    } else {
      displayAtmosphere.print(F("No Probe   "));
    }
    displayAtmosphere.display();

    // Biome display
    displayBiome.setTextColor(SSD1306_WHITE, SSD1306_BLACK);
    displayBiome.setTextSize(1);
    displayBiome.setCursor(0, 0);
    displayBiome.print(F("MANGROVE FOREST   "));
    displayBiome.setCursor(0, 12);
    if (!isnan(biomeTempC)) {
      displayBiome.setTextSize(2);
      displayBiome.print(biomeTempC, 1);
      displayBiome.setTextSize(1);
      displayBiome.print(F("C "));
      displayBiome.setTextSize(2);
      displayBiome.print(biomeTempF, 1);
      displayBiome.setTextSize(1);
      displayBiome.print(F("F "));
    }
    displayBiome.setCursor(0, 35);
    displayBiome.setTextSize(2);
    displayBiome.print(F("RH: "));
    if (!isnan(biomeHum)) {
      displayBiome.print(biomeHum, 1);
      displayBiome.setTextSize(1);
      displayBiome.print(F("%  "));
    }
    displayBiome.display();

    // Telemetry
    if (now - lastTelemetryMs >= TELEMETRY_MS) {
      lastTelemetryMs = now;
      char payload[256];
      snprintf(payload, sizeof(payload),
        "{\"atmo_t\":%.2f,\"atmo_h\":%.1f,\"bio_t\":%.2f,\"bio_h\":%.1f,"
        "\"liq_t\":%.2f,\"pump_pct\":%d,\"target_t\":%.1f}",
        atmoTempC, atmoHum, biomeTempC, biomeHum,
        liquidTempC, pumpPercent, TARGET_TEMP_C
      );
      mqtt.publish(TOPIC_TELEMETRY, payload);
    }
  }
}
