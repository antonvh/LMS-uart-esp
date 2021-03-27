# Remote UART library: uartremote.py

This is a library for robust communication between lego EV3/Spike and other MicroPython modules using the UART.

This is a uniform library that works on standard MicroPython platforms, the EV3 and the Spike. 

## Initialize

Below is an example of how to use this library.

On the slave (ESP8266):

```python
from uartremote import *
u=UartRemote(0)
u.add_command('imu',imu)
u.add_command('led',led)
u.add_command('grid',grideye)
u.loop()
```

In this example two functions are defined `imu`, `led` and `grideye`. These functions are called each time that `imu`, `led` or `grid` is received as a command.  Parameters for the functions are extracted from the command, and return values, are attached to the respons. In practice, these commands will be added to the `boot.py` file on the slave.

## Sending commands

On the master (EV3):
```python
from uartremote import *
u=UartRemote(Port.S1)
u.send_receive('imu')
u.send_receive('grid','B',10)
u.send_receive('led','B',[2,100,100,100])
```
### `send_receive(<cmd>,[<type>,<data>]`
The `send_receive` method allows the Master to send a command to the Slave. When no values need to be passed with the command, the `<type>` and `<data>` can be omitted.  The `<data>` can be a single value, a string or a list of values. The type of `<data>` is given according to the struct Format characters, of which the most commonly used are shown below:

| Format character | type | number of bytes |
|---------------------|-------|--------------|
| `B` | unsigned byte | 1 |
| `H` | unsigned short | 2 |
| `I` | unsigned int | 4 |
| `f` | float | 4 |
| `d` | double | 8 |
| `s` | char[] | 

The Slave acknowledges a command by sending back an acknowledge command, where the string `ack` is appended to the command, and return values of the function being called are are send back. When an error occurs, the `<cmd>` that is sent back, contains `error`.

## packet format
When a command with its accompanying values is transmitted over the Uart, the following packet format is used:

```<l><cl><cmd><fl><f><data>```

with
`l` the length of the total packet encoded as a single byte,
`cl` the length of the command string `<cmd>` as a single byte,
`cmd` the command specified as a string,
`fl` the length of the format string
`f` the Format character used for `struct.pack` to pack the values; when data is a list, the character `a` is prepended to `f`.
`n` the number of `<data>`
`data` a number of values packed using `struct.pack`

When the command
`send_receive('test','B',[1,2,3,4,5]`
is used, the following packet will be transmitted over the line:

```b'\x0e\x04test\x03a5B\x01\x02\x03\x04\x05'```

or in hex:

```0e0474657374036135420102030405```

When the Format string `f` is a single character, and the data is a list, each element of the list will be encoded using the specified Format character. The format field can also consist of multiple Format characters, for example 

```send_receive('special','3b2s1f',1,2,3,"aap",1.3)```.

# Example application
## Slave code
On the slave, the following code is used;
```python
def led(v):
    print('led')
    for i in v:
        print(i)
    
def imu():
    return('f',[12.3,11.1,180.0])

def grideye(v):
    addr=v[0]
    a=[20,21,22,23,24,25,26,27,28]
    return('B',a[addr%9])

from uartremote import *
u=UartRemote(0)
u.add_command("led",led)
u.add_command("imu",imu)
u.add_command("grid",grideye)
u.loop()
```
Here three different example functions are used: `led` which takes a value, but does not return a value, `imu` which returns a value, but does not take a value, and `grideye` wich takes a values and returns a value.
The functions that return a value, need to return a tuple
`<type>, <data>`
with `<type>` the Format character, and where `<value>` can be a string, a single value, or a list of values.

## Master code
On the Master the following code is used:
```python
from uartremote import *
u=Uartremote(Port.S1)
```
In repl the following examples result in:
```
>>> u.send_receive('led','B',[1,2,3,4])
('ledack', [])
>>> u.send_receive('imu')
('imuack', [12.29999923706055, 11.09999847412109, 180.0])
>>> u.send_receive('grid','B',1)
('gridack', [21])
>>> u.send_receive('unknown')
('error', [b'n', b'o', b'k'])
```

# Simultaneous sending and receiving

The library allows for simultaneously sending and receiving commands from both sides. Below the code for both sides is shown. In this example we use the EV3 and the ESP8266 board.

### EV3
```python
import time
from uartremote import *
    
def imu():
    return('f',[12.3,11.1,180.0])

u=UartRemote(Port.S1)
u.add_command("imu",imu)

t_old=time.ticks_ms()+2000                      # wait 2 seconds before starting
q=u.flush()                                     # flush uart rx buffer
while True:
    if u.available():                           # check if a command is available
        u.wait_for_command()
    if time.ticks_ms()-t_old>1000:              # send a command every second
        t_old=time.ticks_ms()
        print("send led")                       # send 'led' command with data
        print("recv=",u.send_receive('led','b',[1,2,3,4]))
```

### ESP8266
```python
import time
from uartremote import *
u=UartRemote(0)

def led(v):
    print('led')
    for i in v:
        print(i)

u.add_command("led",led)


t_old=time.ticks_ms()+2000                      # wait 2 seconds before starting
q=u.flush()                                     # flush uart rx buffer
while True:
    if u.available():                           # check if a command is available
        u.wait_for_command()
    if time.ticks_ms()-t_old>1000:              # send a command every second
        t_old=time.ticks_ms()
        print("send imu")
        print("recv=",u.send_receive('imu'))    # send 'imu' command & receive result
```

# Library description
### `class UartRemote(port,baudrate=115200,timeout=1000,debug=False)`

Constructs a Uart communication class for Uart port `port`. Baudrate and timeout definitions for the Uart port can be changed.  The boolean `debug` allows for debugging this class.

### UartRemote Methods

#### `UartRemote.flush()`

Flushes the read buffer, by reading all remaining bytes from the Uart.

#### `UartRemote.available()`

Return a non zero value if there is a received command available.

#### `UartRemote.send(command,[ t, data])`

Sends a command `command`. When `t` and `data` are omitted, the cooresponding function on the Slave is called with no arguments. Otherwise,`data` is encoded as type `t`, where `command` is a string and `data` is a string or a list of values, or multiple values.

#### `UartRemote.receive()`

Receives a command and returns a tuple `(<command>, <data>)`.  If there is a failure, the `<command>`  will be equal to `'error'`.

#### `UartRemote.send_receive(command)`
#### `UartRemote.send_receive(command,t, data)`
Combines the send and receive functions as defined above. When `t` and `data` are omitted, a dummy value `[]` of type `B` will be send. The parameter `data` can be a string, a single value or a list of values. 

#### `UartRemote.wait_for_command()`

Waits for the reception of a command and returns the received command as a dict `{<command>,<value>}`.

#### `UartRemote.loop()`

Loops the `UartRemote.wait-for_command()` command.

#### `UartRemote.add_command(command,command_function)`

Adds a command `command` to the dictionary of `UartRemote.commands` together with a fucntion name `command_function`. The dictionary with commands is used by the `UartRemote.wait_for_command()` method to call the function as defined upon receiving a specific command. As an argument the `data` that is received is used.
