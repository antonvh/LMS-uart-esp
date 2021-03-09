# LMS-uart-lib

This is a library for robust communication between lego Ev3/Spike and other MicroPython modules using the UART.

The Lego EV3/Spike acts as the master. It initiates the communication with the MicroPython board. 

The MicroPython boards currently supported are the OpenMV H7 and an ESP8266-based micropython board. These boards will act as lave.

## Initialize

Below is an example of how to use this library

```
from uartcmds import *
u=UartComm(0)
u.addcmd('led',led)
u.addcmd('grid',grideye)
```


### `class UartComm`

#### `snd(cmd, value)`

Sends a command `cmd` with `value`, where `cmd` is a string and `value` can be any type value.

#### `rcv()`

Receives a command and returns a struct `{'c':<cmd>, 'v':<value>}`

