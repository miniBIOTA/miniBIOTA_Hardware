#include <Arduino.h>
#include <WiFi.h>
#include <ArduinoOTA.h>
#include <PubSubClient.h>

const char* WIFI_SSID     = "mB2.4";
const char* WIFI_PASS     = "qYKEQe8R763HKmk";
const char* OTA_HOSTNAME  = "biome1-lake";
const char* MQTT_BROKER   = "192.168.8.228";
const int   MQTT_PORT     = 1883;
const char* MQTT_CLIENT   = "biome1-lake";
const char* TOPIC_STATUS  = "miniBIOTA/biome/1/status";

WiFiClient wifiClient;
PubSubClient mqtt(wifiClient);

void connectMQTT() {
  while (!mqtt.connected()) {
    Serial.print("Connecting to MQTT...");
    if (mqtt.connect(MQTT_CLIENT)) {
      Serial.println("connected.");
      mqtt.publish(TOPIC_STATUS, "online");
    } else {
      Serial.print("failed, rc=");
      Serial.print(mqtt.state());
      Serial.println(" retrying in 5s");
      delay(5000);
    }
  }
}

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
  ArduinoOTA.onStart([]() { Serial.println("OTA start"); });
  ArduinoOTA.onEnd([]()   { Serial.println("OTA done");  });
  ArduinoOTA.onError([](ota_error_t error) {
    Serial.printf("OTA error [%u]\n", error);
  });
  ArduinoOTA.begin();
  Serial.println("OTA ready.");

  mqtt.setServer(MQTT_BROKER, MQTT_PORT);
  connectMQTT();
}

void loop() {
  ArduinoOTA.handle();

  if (!mqtt.connected()) connectMQTT();
  mqtt.loop();
}
