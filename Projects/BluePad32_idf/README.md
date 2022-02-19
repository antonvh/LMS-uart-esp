# BluePad32 for Lego robot

## Precompiled binary
The file `bluepad32_firmware.bin` contains the precompiled binary that can be flashed on the LMD-ESP32 board using this commands:

```
esptool.py -p <port> erase_flash
esptool.py -p <port> --baud 500000 write_flash 0x1000 bluepad32_firmware.bin
```

Connect the LMS-ESP32 module to your Spike PRIME or Robot Inventor and run the program `bluepad32_spike.py` in the `SPIKE` directory.

Once the controller is connected, you should see two dots on the robot 5x5 display, where each dot can be controlled by one of the analogue joysticks. When the left button on the robot is pressed, the LEDs on the controller are incremented by one. By pressing the right button on the robot activates the rumble of the controller.

## Installation of ESP-IDF

Install esp-idf as described here https://docs.espressif.com/projects/esp-idf/en/stable/esp32/get-started/#get-started-get-esp-idf also there is a handy VSCode plugin with additional ways  to get the IDF setup https://github.com/espressif/vscode-esp-idf-extension/blob/master/docs/tutorial/install.md

you must have idf.py working to continue open a shell/console and test the following command:

`. ~/esp/esp-idf/export.sh`

you should have seen something like: *Done! You can now compile ESP-IDF projects. Go to the project directory and run: idf.py build.* If so you are ready to proceed, if not you must correct the issues.

## Set-up of IDF-ESP32-Arduino with BluePad32 and UartRemote

Quick-start with this project https://github.com/ricardoquesada/bluepad32/blob/main/docs/plat_arduino.md we used option A. This will setup a IDE with BluePad32 and its requirements including Aduino. For more troubleshooting or details on the Aduino on ESP32 see [here](https://github.com/espressif/arduino-esp32)

From your command shell where you have esp-idf ready (install step) enter the working directory of LMS-uart-esp/Projects/BluePad32_idf and clone the esp-idf-arduino-bluepad32-template.git into a new folder BluePad32_Uartremote

```
cd LMS-uart-esp/Projects/BluePad32_idf
git clone --recursive https://gitlab.com/ricardoquesada/esp-idf-arduino-bluepad32-template.git BluePad32_Uartremote
```

This is a large download (~2GB) When download is done, you can take time to build this vanilla project to test your full IDE enviroment issuing a `idf.py build` in the Bluepad32_uartremote directory, this was described in the Quick-Start document above as well, you dont need to do it twice but you can `idf.py clean`. Also noteworthy you can [config](https://github.com/ricardoquesada/bluepad32/blob/main/docs/plat_arduino.md#update-configuration) `idf.py menuconfig` from here to modify components. Build should pass with no halting errors, you will want to correct or fix anything before proceeding (it is out of scope here, bluepad32 has a discord support channel) if you saw something like *Project build complete. To flash* then your good, go back a directory to continue.

still in  `LMS-uart-esp/Projects/BluePad32_idf`

copy in the uartremote component and modified aduino_main into BluePad32_uartremote

```
cp -a main BluePad32_Uartremote
cp -a components BluePad32_Uartremote
```

You are now ready to build the full project with included uartremote, this will build, flash and monitor your ESP32

```
cd BluePad32_uartremote
idf.py build
```

Update for your device and flash your ESP32 with the uartremote, bluepad firmware!

```
idf.py -p /dev/ttyUSB0 flash
idf.py -p /dev/ttyUSB0 monitor
```
exit monitor with ctl+]

## On Lego Spike Prime or Mindstorms Robot Inventor

to setup a remote see here https://github.com/ricardoquesada/bluepad32/blob/main/docs/supported_gamepads.md for list of supported devices.

press connect on your remote while watching the ESP32 monitor you should see the device connect *Gamepad is connected!* success!

Use example uPython code in `LMS-uart-esp/Projects/BluePad32_idf/SPIKE/bluepad32.py` on your Lego Hub


## Development Notes

you can edit `Projects/BluePad32_idf/BluePad32_Uartremote/main/arduino_main.cpp` like you would your Arduino/main
for example you could add 

[menuconfig](https://github.com/ricardoquesada/bluepad32/blob/main/docs/plat_arduino.md#update-configuration) details


### Add Wifi AP
The following requires advanced use with `idf.py menuconfig` to increse the memory space available in the build process.

the menu option needed to change is as follows:
* Partition table >>> Partition Table (Single factory app (large), no OTA) >>> ENTER
  * you should see Single factory app (large), no OTA, 
    * select it and press enter 
      * then 'S' then enter to save config and exit


* enable Component config > HTTP Server > WebSocket server support

if further configs are needed but is advanced please see..
* https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/kconfig.html#config-httpd-ws-support
* https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/protocols/esp_http_server.html


edit arduino_main.cpp with the following:
```
// Wifi
#include <WiFi.h>

// Replace with your network credentials
const char* ssid     = "LEGO-ESP32";
const char* password = "legoesp32";

// Set web server port number to 80
WiFiServer server(80);

// Variable to store the HTTP request
String header;

##
## this is not a direct cut and paste
void setup() { # the following is for setup loop
    // Setup wifi AP
    WiFi.softAP(ssid, password);
    IPAddress IP = WiFi.softAPIP();
    Serial.print("AP IP address: ");
    Serial.println(IP);
```

once this is modified `idf.py clean` and `idf.py build`

### Add your 3rd party Arduino libraries:

To include 3rd party Arduino libraries in your project, you have to:
* Add them to the components folder.
  * Add a CMakeLists.txt inside the component's folder 

You can quickly test by adding your library in components/arduino/libraries and modify components/arduino/CMakeLists.txt 

#### Example ESP32Servo [ESP32Servo](https://gitlab.com/ricardoquesada/esp-idf-arduino-bluepad32-template#example-adding-esp32servo)


in  `/LMS-uart-esp/Projects/BluePad32_idf/BluePad32_Uartremote/components`

```
git clone https://github.com/madhephaestus/ESP32Servo.git
cd ESP32Servo
cat << EOF > component.mk
COMPONENT_ADD_INCLUDEDIRS := src
COMPONENT_SRCDIRS := src
EOF
cat << EOF > CMakeLists.txt
idf_component_register(SRC_DIRS "src"
                    INCLUDE_DIRS "src"
                    REQUIRES "arduino")
EOF
```

now in `/LMS-uart-esp/Projects/BluePad32_idf/BluePad32_Uartremote/main`

edit CMakeLists.txt to incluide the following

* REQUIRES "${requires}" "UartRemote" `"ESP32Servo"`)

Add this include in your arduino_main.cpp file
`#include <ESP32Servo.h>`

now compile with `idf.build` from the /LMS-uart-esp/Projects/BluePad32_idf/BluePad32_Uartremote/ location


#### example using [UartRemote-Aduino](https://github.com/antonvh/UartRemote/tree/master/Arduino) 

* copied UartRemote-Arduino into components/arduino/libraries

in components/arduino/CMakeLists.txt make the following changes:

under

```
set(LIBRARY_SRCS
```

add:

```
  libraries/UartRemote/src/UartRemote.cpp
  libraries/UartRemote/src/struct.c
  libraries/UartRemote/src/struct_endian.c

```

under

```
set(includedirs
  variants/${IDF_TARGET}/
  cores/esp32/
```

add:

```
libraries/UartRemote/src
```
