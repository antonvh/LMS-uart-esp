# ESP8266

Hook up a neopixel array where

|ESP8266|LMS-connector-board|Neopixel|
|-------|-------------------|--------|
|GPIO4 | SDA | Din|
|      | GND | GND |
|      | Vin | VCC +5V|


# demo

## on ESP8266
Run the demo by uploading `neo_ESP8266.py` to the ESP8266 module and by executing:

```
from neo_ESP8266 import *
```

This will initiate the `loop` method of the `UartRemote` class, waiting for commands to be received through the UART.

## on EV3

Upload `neo_EV3.py` to the EV3 and execute:

```
from neo_EV3 import *

neo=Neo(u,8)

n=0
while True:
    neo.set_pixel(n%8,(100,100,0))
    neo.set_pixel(n%8,(0,0,0))
    n+=1
```

# Code explained

##`neo_ESP8266.py`

```
import neopixel,machine

from uartremote import *

np=[]

def neo_init(number_pixels,pin=machine.Pin(4)):
    global np
    np = neopixel.NeoPixel(pin, number_pixels)
    return 'ok'

def neo_setpixel(pix):
    global np
    n=pix['n']
    (r,g,b)=pix['c']
    np[n]=(r,g,b)
    np.write()
    return 'ok'

u=UartRemote(0)
u.add_command('neo',neo_init)
u.add_command('neo_set',neo_setpixel)
u.loop()
```

The function `neo_init` initializes a neopixel with a number of pixels `number_pixels` on default pin `Pin(4)` and stores the result in a global structure `np`. 

The function `set_setpixel` sets the color value of a specific value using the dict `pix` which contains `{'n':<pixel>,'c'<color>:}` with `pixel` the index of the pixel to set and `<color>` the RGB color as a tuple `(<r>,<g>,<b>)`.

The UartRemote class is instantiated and a two commands are defined with the `add_command` method, where the function `neo_init` is mapped on the command string `'neo'` and `neo_setpixel` is mapped on the command string `'neo_set'`.

The `u.loop()` command waits for a command to be received through the UART and executes the commmand.

##`neo_EV3.py`

```
from uartremote import *
u=UartRemote(Port.S1)
from time import sleep

class Neo:
    uart_remote=1
    
    def __init__(self,uart_remote,number_pixels):
        self.number_pixels=number_pixels
        self.uart_remote=uart_remote
        self.uart_remote.send_receive('neo',number_pixels)
    
    def set_pixel(self,pixel,color):
        self.uart_remote.send_receive('neo_set',{'n':pixel,'c':color})

    def off(self):
        for i in range(self.number_pixels):
            self.uart_remote.send_receive('neo_set',{'n':i,'c':(0,0,0)})



neo=Neo(u,8)

n=0
while True:
    neo.set_pixel(n%8,(100,100,0))
    neo.set_pixel(n%8,(0,0,0))
    n+=1

 
```

In this example, a class `Neo` is defined with a method `init` to initialize a NeoPixel array with a number of pixels `number_pixels`. Note that the `uart_remote` is passed as a parameter, a method `set_pixel` to set a pixel to a color `(<r>,<g>,<b>)`, and a method `off` to turn all NeoPixels off.
