# Old uartremote.py library

This is a library for robust communication between lego EV3/Spike and other MicroPython modules using the UART.

This is a uniform library that works on standard MicroPython platforms, the EV3 and the Spike. 

## Initialize

Below is an example of how to use this library.

On the slave (ESP8266):

```
from uartremote import *
u=UartRemote(0)
u.add_command('led',led)
u.add_command_('grid',grideye)
u.loop()
```

In this example two functions are defined `led` and `grideye`. These functions are called each time that `led` or `grid` is received as a command. In practice, these commands will be added to the `boot.py` file on the slave.

On the master (EV3):
```
from uartcommands import *
u=UartRemote(Port.S1)
u.send_receive('grid',10)
u.send_receive('led',[[100,100,100],[100,0,0],[0,0,100]])
```


### `class UartRemote(port,baudrate=115200,timeout=1000,debug=False)`

Constructs a Uart communication class for Uart port `port`. Baudrate and timeout defitions for the Uart port can be changed. De boolean `debug` allows for debugging this class.

### UartRemote Methods

#### `UartRemote.send(command, value)`

Sends a command `command` with `value`, where `command` is a string and `value` can be any type value.

#### `UartRemote.receive()`

Receives a command and returns a struct `{'c':<command>, 'v':<value>}`. It returns the receveid command as a dict `{<command>,<value>}`. If there is a failure, the value will be equal to `'nok'`.

#### `UartRemote.send_receive(command,value)`

Combines the send and receive functions as defined above.

#### `UartRemote.wait_for_command()`

Waits for the reception of a command and returns the received command as a dict `{<command>,<value>}`.

#### `UartRemote.loop()`

Loops the `UartRemote.wait-for_command()` command.

#### `UartRemote.add_command(command,command_function)`

Adds a command `command` to the dictionary of `UartRemote.commands` together with a fucntion name `command_function`. The dictionary with commands is used by the `UartRemote.wait_for_command()` method to call the function as defined upon receing a speicific command. As an argument the `value` that is received is used.
