# LPF2 Lego Power Function protocol

[On this GutHub](https://github.com/ceeoinnovations/SPIKEPrimeBackpacks/tree/master/examples) you will find code for the so-called SPIKE backpack (ultrasone sensor chasis connected to diffrent platforms).

The code in this drectory is a proof of concept showing that the simplistic microbit implemenation can be adopted to work with the ESP8266.

## run test

Upload `lpf2_esp.py` and `lpf2_esp_ex.py` on the ESP8266. Execute `lpf2_SPIKE.py` on the SPIKE prime. In this example the 'sensor' counts repeatedly from 0 to 9. The SPIKE receives this number and displays it on the screen.
The ESP8266 emulates a UltraSonic sensor (type 62=0x3e).

## Extensive LPF2 class (in LPF2 folder)
This class allows for configuration of the sensor. It supports multple modes per sensor. 

### problems with Timer

In porting the file `LPF2.py` to the ESP8266 problems occur with the Timer object. needs to be solved. 