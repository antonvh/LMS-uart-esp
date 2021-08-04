# Precision Hall Effect Angle Sensor

## Hardware

The sensor we are using is an Allegro Hall-effect sensor. The sensor uses the Circular Vertical Hall techcan detect the 
## I2C reading of angle

```
from machine import I2C, Pin
import struct
from time import sleep_ms

i2c=I2C(scl=Pin(5),sda=Pin(4))

def read_angle(sensor):
    return struct.unpack(">H",i2c.readfrom_mem(sensor,0x20,2))[0]&0xfff

while True:
    sleep_ms(100)
    print(read_angle(12),read_angle(14))
```
