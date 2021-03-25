# VL53 Time of Flight sensor

We use the standard VL53 micropython library. This library is too big to fit in the memory of the ESP8266. Therefore, we use the pre-compiled version: vl53.mpy.
The library as compikled using the following command:

```./mpy-cross -march=xtensa vl53.py -o vl53.mpy```

`mpy-cross` is a standard tool that comes with the micropython distribution. The tool can be installed using:

```
pip3 install mpy-cross
```

## example ESP8266, using uartfast

```python
from uartfast import *
from vl53 import *

u=UartRemote(0)

from machine import I2C,Pin
i2c=I2C(scl=Pin(5),sda=Pin(4))
tof=VL53L0X(i2c)    
tof.start()

def vl53():
  d=tof.read()
  return ('i',d) # return integer
  
u.add_command('vl53',vl53)
 
u.loop()
```

## example EV3, using uartfast

```python
import time
from uartfast import *
u=UartRemote(Port.S1)

while True:
    r,value=u.send_receive('vl53') 
    print(value)
    time.sleep(1)
```    
