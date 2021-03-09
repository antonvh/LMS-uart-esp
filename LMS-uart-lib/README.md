# LMS-uart-lib

This is a library for robust communication between lego EV3/Spike and other MicroPython modules using the UART.

This is a uniform library that works on standard MicroPython platforms, the EV3 and the Spike. 

## Initialize

Below is an example of how to use this library.

On the slave (ESP8266):

```
from uartcmds import *
u=UartComm(0)
u.addcmd('led',led)
u.addcmd('grid',grideye)
u.loop()
```

In this example two functions are defined `led` and `grideye`. These functions are called each time that `led` or `grid` is received as a command. In practice, these commands will be added to the `boot.py` file on the slave.

On the master (EV3):
```
from uartcmds import *
u=UartComm(Port.S0)
u.sndrcv('grid',10)
u.sndrcv('led',[[100,100,100],[100,0,0],[0,0,100]])
```


### `class UartComm(port,baudrate=115200,timeout=1000,debug=False`

Constructs a Uart communication class for Uart port `port`. Baudrate and timeout defitions for the Uart port can be changed. De boolean `debug` allows for debugging this class.

### UartComm Methods

#### `UartComm.snd(cmd, value)`

Sends a command `cmd` with `value`, where `cmd` is a string and `value` can be any type value.

#### `UartComm.rcv()`

Receives a command and returns a struct `{'c':<cmd>, 'v':<value>}`. It returns the receveid command as a dict `{<cdm>,<value>}`. If there is a failure, the value will be equal to `'nok'`.

#### `UartComm.sndrcv(cmd,value)`

Combines the send and receive functions as defined above.

#### `UartComm.waitcmd()`

Waits for the reception of a command and returns the received command as a dict `{<cmd>,<value>}`.

#### `UartComm.loop()`

Loops the `UartComm.waitcmd()` command.

#### `UartComm.addcmd(cmd,cmd_function)`

Adds a command `cmd` to the dictionary of `UartComm.cmds` together with a fucntion name `cmd_function`. The dictionary with commands is used by the `UartComm.waitcmd()` method to call the function as defined upon receing a speicific command. As an argument the `value` that is received is used.
