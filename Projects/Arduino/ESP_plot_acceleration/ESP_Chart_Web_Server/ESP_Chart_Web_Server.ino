/*********
  Rui Santos
  Complete project details at https://RandomNerdTutorials.com
  
  Permission is hereby granted, free of charge, to any person obtaining a copy
  of this software and associated documentation files.
  
  The above copyright notice and this permission notice shall be included in all
  copies or substantial portions of the Software.
*********/

// Import required libraries
#ifdef ESP32
  #include <WiFi.h>
  #include <ESPAsyncWebServer.h>
  #include <SPIFFS.h>
#else
  #include <Arduino.h>
  #include <ESP8266WiFi.h>
  #include <Hash.h>
  #include <ESPAsyncTCP.h>
  #include <ESPAsyncWebServer.h>
  #include <FS.h>
#endif
#include "UartRemote.h"

/*#include <SPI.h>
#define BME_SCK 18
#define BME_MISO 19
#define BME_MOSI 23
#define BME_CS 5*/


// Replace with your network credentials
const char* ssid = "....";
const char* password = "....";

// Create AsyncWebServer object on port 80
AsyncWebServer server(80);

#include "UartRemote.h"
char cmd[20]; // global temporary storage for command names
UartRemote uartremote;

float ax=0,ay=0,az=0;

void readimu() {
  uartremote.send("imu","b",0); // send with dummy byte
  if (uartremote.available()>0) {
    unpackresult rcvunpack = uartremote.receive(cmd);
    printf("received v alues for command %s\n",cmd);
    uartremote.getvariables(rcvunpack,&ax,&ay,&az);
    printf("acc ax=%f, ay=%f , az=%f\n",ax,ay,az);
  }
  
}
String readax() {
  // Read temperature as Celsius (the default)
  readimu();
  // Convert temperature to Fahrenheit
  //t = 1.8 * t + 32;
  if (isnan(ax)) {    
    Serial.println("Failed to read from BME280 sensor!");
    return "";
  }
  else {
    Serial.println(ax);
    return String(ax);
  }
}

String readay() {
  //readimu();
  if (isnan(ay)) {
    Serial.println("Failed to read from BME280 sensor!");
    return "";
  }
  else {
    Serial.println(ay);
    return String(ay);
  }
}

String readaz() {
  //readimu();
  if (isnan(az)) {
    Serial.println("Failed to read from BME280 sensor!");
    return "";
  }
  else {
    Serial.println(az);
    return String(az);
  }
}

void setup(){
  // Serial port for debugging purposes
  Serial1.begin(230400, SERIAL_8N1, RXD1, TXD1);
  // debug 
  Serial.begin(115200);

 
  // Initialize SPIFFS
  if(!SPIFFS.begin()){
    Serial.println("An Error has occurred while mounting SPIFFS");
    return;
  }

  // Connect to Wi-Fi
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(1000);
    Serial.println("Connecting to WiFi..");
  }

  // Print ESP32 Local IP Address
  Serial.println(WiFi.localIP());

  // Route for root / web page
  server.on("/", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send(SPIFFS, "/index.html");
  });
  server.on("/ax", HTTP_GET, [](AsyncWebServerRequest *request){
    //const char* res = readax();
    request->send_P(200, "text/plain", readax().c_str());
  });
  server.on("/ay", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", readay().c_str());
  });
  server.on("/az", HTTP_GET, [](AsyncWebServerRequest *request){
    request->send_P(200, "text/plain", readaz().c_str());
  });

  // Start server
  server.begin();
}
 
void loop(){
  
}
