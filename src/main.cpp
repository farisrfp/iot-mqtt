#include <Arduino.h>
#include <WiFi.h>
#include <PubSubClient.h>
#include <TinyGPSPlus.h>

// Change the credentials below
const char *ssid = "VI-ROSE";
const char *password = "VIROSEJUARA1";
const char *mqtt_server = "192.168.1.102";
const char *mqtt_user = "user";
const char *mqtt_password = "admin";

// Object for declaring for GPS and MQTT
TinyGPSPlus gps;
WiFiClient espClient;
PubSubClient client(espClient);

// Timers auxiliar variables
long now = millis();
long lastMeasure = 0;

// GPS variables including time
float latitude = 0;
float longitude = 0;
int year, month, day, hour, minute, second;

// Buffer for serial formatting debug
char buffer[100];

// Function Prototypes
#include "Function.h"

void setup()
{
  // Set Baundrate for Serial/UART communication
  Serial.begin(115200);
  Serial2.begin(9600);
  // Setup ESP32 for MQTT
  pinMode(LED_BUILTIN, OUTPUT);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
}
  
void loop() {
  // Reconnects to MQTT broker if connection is lost
  if (!client.connected())  reconnect();
  if (!client.loop())       client.connect("ESP8266Client");

  // Publishes GPS values
  while(Serial2.available() > 0) {
    gps.encode(Serial2.read());
    // GPS
    if (gps.location.isUpdated()){
      latitude = gps.location.lat();
      longitude = gps.location.lng();
      sprintf(buffer, "Latitude: %f, Longitude: %f", latitude, longitude);
      client.publish("gps/latitude", String(latitude).c_str());
      client.publish("gps/longitude", String(longitude).c_str());
      Serial.println(buffer);
    }
    // Date
    if (gps.date.isUpdated()){
      year = gps.date.year();
      month = gps.date.month();
      day = gps.date.day();
      sprintf(buffer, "Year: %d, Month: %d, Day: %d", year, month, day);
      client.publish("gps/date", String(buffer).c_str());
      Serial.println(buffer);
    }
    // Time
    if (gps.time.isUpdated()){
      hour = gps.time.hour();
      minute = gps.time.minute();
      second = gps.time.second();
      sprintf(buffer, "Hour: %d, Minute: %d, Second: %d", hour, minute, second);
      client.publish("gps/time", String(buffer).c_str());
      Serial.println(buffer);
    }
  }
} 