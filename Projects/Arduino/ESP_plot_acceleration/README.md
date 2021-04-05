# Example using AsyncWebserver

## Setup ESP32 <-> ESP8266

For running this demo, I hooked up the LMS-esp-Wifi board to an ESP32. The ESP8266 runs Micropython, the ESP32 is programmed using Arduino.

The ESP8266 is connected to a `mpu9250` IMU sensor. The Python code waits for a command recevied though the UartRemote and sens back the acceleration values for `ax, ay, az`.

The ESP32 runs a webserver.

### connections
 
|ESP32 | ESP8266 | MPU9250|
|------|--------|---------|
|GND  | GND| GND|
|5V  | Vin| |
|TX GPIO19| RX | |
|RX GPIO18| TX| |
| | GPIO4 SDA | SDA |
| | GPIO4 SCL | SCL |


 
## Installation

Install `ESPAsyncWebServer-master.zip` under Libraries, install as .zip.

This example uses SPIFFS file system. You need to install the tool for uploading files in Arduino. See (https://randomnerdtutorials.com/install-esp32-filesystem-uploader-arduino-ide/)