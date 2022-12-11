#include <Arduino.h>
#include <TinyGPSPlus.h>

// The TinyGPS++ object
TinyGPSPlus gps;

void setup(){
  Serial.begin(9600);
  Serial2.begin(9600);
}

void loop(){
  // This sketch displays information every time a new sentence is correctly encoded.
  while (Serial2.available() > 0){
    gps.encode(Serial2.read());
    if (gps.location.isUpdated()){
      Serial.print("Latitude= "); 
      Serial.print(gps.location.lat(), 6);
      Serial.print(" Longitude= "); 
      Serial.println(gps.location.lng(), 6);
    }
  }
}