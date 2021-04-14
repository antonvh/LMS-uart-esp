# LPF2 Lego Power Function protocol

[On this GutHub](https://github.com/ceeoinnovations/SPIKEPrimeBackpacks/tree/master/examples) you will find code for the so-called SPIKE backpack (ultrasone sensor chasis connected to diffrent platforms).

The code in this drectory is a proof of concept showing that the simplistic microbit implemenation can be adopted to work with the ESP8266.

## counting test

Upload `LPF2_esp.py` and `LPF2_test.py` on the ESP8266. Execute `lpf2_SPIKE.py` on the SPIKE prime. In this example the 'sensor' counts repeatedly from 0 to 9. The SPIKE receives this number and displays it on the screen.
The ESP8266 emulates a UltraSonic sensor (type 62=0x3e).

## Example woth TOF VL53
Upload `LPF2_esp.py` and `LPF2_tof.py`. You also need the `vl53.mpy` library from the TOF Project. Connect a vL53x sensor to the i2c port of the ESP board. Place LPF2_tof.py in main.py to automatically start the sensor. Now, the sensor can be used in standard Lego Education Spike Prime environement, or from micropython.

