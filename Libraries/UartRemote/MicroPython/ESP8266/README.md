= Compiled uartremote library for ESP8266

In this directory you find the latest version of uartremote compiled for ESP8266 in `uartremote.mpy`. Yu can copy this file to the ESP8266 module.

== Firmware

When compiling the Micropython firmware with the `uartremote` compiled as frozen module has the advantage that the module uses far less RAM memory as compared to loading the `uartremote.mpy` module from flash.

All that is needed, is to copyt the `uartremote.py` file in de `/ports/esp8266/modules` directory and build the firmware. The firmware `micropython-v1.15-uartremote.bin` is version MicroPython v1.15 and can be flashed on the ESP8266 board, as described in the Wiki.
