# LPF2 Lego Power Function protocol

[On this GutHub](https://github.com/ceeoinnovations/SPIKEPrimeBackpacks/tree/master/examples) you will find code for the so-called SPIKE backpack (ultrasone sensor chasis connected to diffrent platforms).

The code in this drectory is a proof of concept showing that the OpenMV MicroPython code can be adopted to work with the ESP8266. The library can be foud in the file `LPF2_esp.py`.

The original Lego Sensors, such as the color sensor and the distance sensor of the SPIKE Prime, use a Lego proprietary protocol, called LPF2. This protocol deploys the UART to communicate with the sensor. The communication initates at 2400 baud and is further increased to typically 115200 baud. Furthermore, the sensor can advertise its capabilities to the Lego Hub. These capabilities are advertised in so-called modes of operation. Per mode, the unit, the range in this unit, the range of the raw sensor and the range in percentage is communicated. Also the capability of the sensor to receive data from the hub is laid down in the advertisement message of that mode. The EV3 hub supports a subset of the LPF2 protocol as supported bu the SPIKE prime platform.

## Further information

A [good desciption](https://github.com/pybricks/technical-info/blob/master/uart-protocol.md) of the protocol can be found in the PyBricks documentation 

The LPF2 protocol for the EV3 is very similar to that for the SPIKE. A description of this subset can be found in the links below, and can be helpfull for understanding the protocol as a whole:
- [UART protocol spoken by LEGO EV3 sensors](https://sourceforge.net/p/lejos/wiki/UART%20Sensor%20Protocol/)
- [An Arduino implementatie for the EV3 protocol](https://github.com/lawrie/EV3_Dexter_Industries_Sensors/tree/master/EV3_arduino)
- https://www.philohome.com/wedo2reverse/wedo2.htm

## LMS-ESP32 library

the file `LPF2_esp32.py` needs to be loaded on the LMS-ESP32 board. A small demo is provided where `LPF2_test_esp32.py` need to be run on the LMS-ESP32 board. This implements a sensor with 3 modes. Mode 0 is a counter from 0 to 9, Mode 1 is a counter, but multiplies with 1001, counting from 0 to 9009, and Mode 3 is a float where the count value is multiplies with 1.001.
On the SPIKE prime, the program `LPF2_SPIKE_test_esp32.py` switches modes from the emulated sensor and shows the read out of the value.

## counting test

To prevent interference of the repl prompt that can be active on the UART and the usage of the UART for the LP2 protocols, the repl prompt should be disabled on the ESP8266 board by uncommenting the flolowing line in the `boot.py` file:

```
uos.dupterm(None, 1)
```

Upload `LPF2_esp.py` and `LPF2_test.py` on the ESP8266. Execute `lpf2_SPIKE.py` on the SPIKE prime. In this example the 'sensor' counts repeatedly from 0 to 9. The SPIKE receives this number and displays it on the screen.
The ESP8266 emulates a UltraSonic sensor (type 62=0x3e).

## Example woth TOF VL53
Upload `LPF2_esp.py` and `LPF2_tof.py`. You also need the `vl53.mpy` library from the TOF Project. Connect a vL53x sensor to the i2c port of the ESP board. Place LPF2_tof.py in main.py to automatically start the sensor. Now, the sensor can be used in standard Lego Education Spike Prime environement, or from micropython.

