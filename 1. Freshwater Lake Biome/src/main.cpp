#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoOTA.h>

const char* WIFI_SSID = "mB2.4";
const char* WIFI_PASS = "qYKEQe8R763HKmk";
const char* OTA_HOSTNAME = "biome1-lake";

void setup() {
  Serial.begin(115200);
  delay(500);

  Serial.print("Connecting to ");
  Serial.println(WIFI_SSID);

  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASS);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected. IP: ");
  Serial.println(WiFi.localIP());

  ArduinoOTA.setHostname(OTA_HOSTNAME);

  ArduinoOTA.onStart([]() {
    Serial.println("OTA start");
  });
  ArduinoOTA.onEnd([]() {
    Serial.println("OTA done");
  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("OTA error [%u]\n", error);
  });

  ArduinoOTA.begin();
  Serial.println("OTA ready.");
}

void loop() {
  ArduinoOTA.handle();
}
