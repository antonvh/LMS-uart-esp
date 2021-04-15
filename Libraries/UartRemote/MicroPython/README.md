# Remote UART library: uartremote.py

This is a library for robust communication between lego EV3/Spike and other MicroPython modules using the UART.

This is a uniform library that works on standard MicroPython platforms, the EV3 and the Spike. 

## ESP8266: Disable repl on UART

For this library to work properly, the repl prompt duplication on the UART needs to be disabled. Therefore, make the following change in `boot.py`

```
...
import uos, machine
uos.dupterm(None, 1) # disable REPL on UART(0)
...
```
## Spike prime: uploading the library
In order to upload the UartRemote library to the Spike Prime hub, it is convenient to install the `rshell` Python extension by:

```
pip3 install rshell
```

Hook up the Spike prime Hub and identyfy the Serial port on the PC to which the hub is connected. On Windoew,e.g. COMxx on Mac OSX, /dev/tty.xxxxxx, and on Linux, /dev/ttyACMx.

Start the rshell, and connect to the hub, where `<serial port>` is the port as identified above:

```
rshell
connect serial <serial port>
```

You can now copy the library to the hub by issueing the following `rshell` command:

```
cp <path_to_library>/uartremote.py /pyboard/.
```

Note: On Windows use backslashes (`\`) in the `<path_to_library>`.

Now you can either use the Spike programming environment, or start a repl prompt from the `rshell`:

```
repl
```
## Initialize

Below is an example of how to use this library.

On the slave (ESP8266):

```python
from uartremote import *
u=UartRemote(0)
u.add_command('imu',imu,'f')
u.add_command('led',led)
u.add_command('grid',grideye,'f')
u.loop()
```

In this example two functions are defined `imu`, `led` and `grideye`. These functions are called each time that `imu`, `led` or `grid` is received as a command.  Parameters for the functions are extracted from the command, and return values, are attached to the respons. In practice, these commands will be added to the `boot.py` file on the slave.

## Sending commands

On the master (EV3):
```python
from uartremote import *
u=UartRemote(Port.S1)
u.send_command('imu')
u.send_command('grid','B',10)
u.send_command('led','B',[2,100,100,100])
```
### `send_command(<cmd>,[<type>,<data>])`
The `send_command` method allows the Master to send a command to the Slave. When no values need to be passed with the command, the `<type>` and `<data>` can be omitted.  The `<data>` can be a single value, a string or a list of values. The type of `<data>` is given according to the struct Format characters, of which the most commonly used are shown below:

| Format character | type | number of bytes |
|---------------------|-------|--------------|
| `b` | byte | 1 |
| `B` | unsigned byte | 1 |
| `i` | int | 4 |
| `I` | unsigned int | 4 |
| `f` | float | 4 |
| `d` | double | 8 |
| `s` | char[] | 

The Slave acknowledges a command by sending back an acknowledge command, where the string `ack` is appended to the command, and return values of the function being called are sent back. When an error occurs, the `<cmd>` that is sent back, contains `error`.

When the Format string `f` is a single character, and the data is a list, each element of the list will be encoded using the specified Format character. The format field can also consist of multiple Format characters, for example 

```send_command('special','3b3s1f',1,2,3,"aap",1.3)```.

# Example application
## Slave code
On the slave, the following code is used;
```python
def led(v):
    print('led')
    for i in v:
        print(i)
    
def imu():
    return([12.3,11.1,180.0])

def grideye(v):
    addr=v
    a=[20,21,22,23,24,25,26,27,28]
    return(a[addr%9])

from uartremote import *
u=UartRemote(0)
u.add_command("led",led)
u.add_command("imu",imu,'f')
u.add_command("grid",grideye,'B')
u.loop()
```
Here three different example functions are used: `led` which takes a value, but does not return a value, `imu` which returns a value, but does not take a value, and `grideye` wich takes a values and returns a value.
In the `add_command` method, the second argument is the `formatstring`, defining the format of the return argument9s).

## Master code
On the Master the following code is used:
```python
from uartremote import *
u=Uartremote(Port.S1)
```
In repl the following examples result in:
```
>>> u.send_receive_command('led','B',[1,2,3,4])
('ledack', [])
>>> u.send_receive_command('imu')
('imuack', [12.29999923706055, 11.09999847412109, 180.0])
>>> u.execute_command('grid','B',1)
('gridack', [21])
>>> u.send_receive_command('unknown')
('error', [b'nok'])
```

# Simultaneous sending and receiving

The library allows for simultaneously sending and receiving commands from both sides. Below the code for both sides is shown. In this example we use the EV3 and the ESP8266 board.

### EV3
```python
import time
from uartremote import *
    
def imu():
    return([12.3,11.1,180.0])

u=UartRemote(Port.S1)
u.add_command("imu",imu,'f')

t_old=time.ticks_ms()+2000                      # wait 2 seconds before starting
q=u.flush()                                     # flush uart rx buffer
while True:
    if u.available():                           # check if a command is available
        u.execute_command(wait=False)
    if time.ticks_ms()-t_old>1000:              # send a command every second
        t_old=time.ticks_ms()
        print("send led")                       # send 'led' command with data
        print("recv=",u.send_receive_command('led','b',[1,2,3,4]))
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
        u.execute_command(wait=False)
    if time.ticks_ms()-t_old>1000:              # send a command every second
        t_old=time.ticks_ms()
        print("send imu")
        print("recv=",u.send_receive_command('imu'))    # send 'imu' command & receive result
```

# Library description
### `class UartRemote(port,baudrate=115200,timeout=1000,debug=False)`

Constructs a Uart communication class for Uart port `port`. Baudrate and timeout definitions for the Uart port can be changed.  The boolean `debug` allows for debugging this class.

### UartRemote Methods

#### `UartRemote.flush()`

Flushes the read buffer, by reading all remaining bytes from the Uart.

#### `UartRemote.available()`

Return a non zero value if there is a received command available.

#### `UartRemote.send_command(command,[ t, data])`

Sends a command `command`. When `t` and `data` are omitted, the cooresponding function on the Slave is called with no arguments. Otherwise,`data` is encoded as type `t`, where `command` is a string and `data` is a string or a list of values, or multiple values.

#### `UartRemote.receive_command(wait=True)`

Receives a command and returns a tuple `(<command>, <data>)`.  If there is a failure, the `<command>`  will be equal to `'err'`. If `wait` is True, the methods waits until it receives a command. 

#### `UartRemote.send_receive_command(command)`
#### `UartRemote.send_receive_command(command,t, data)`
Combines the send and receive functions as defined above. When `t` and `data` are omitted, a dummy value `[]` of type `B` will be send. The parameter `data` can be a string, a single value or a list of values. 

#### `UartRemote.execute_command(wait=True,check=True)`

If `wait` is True, this medthods Waits for the reception of a command, otherwise, it immediately starts receiving a command. Is the flasg `check` is True, it checks for errors or for an `ack` of onother command. It then calls the function corresponding with the received command (prior set by `add_command`) and sends back the result of the executed function.

#### `UartRemote.loop()`

Loops the `UartRemote.wait-for_command()` command.

#### `UartRemote.add_command(command,command_function[,format_string])`

Adds a command `command` to the dictionary of `UartRemote.commands` together with a function name `command_function`. Optionally, if the `command_function` returns parameters, the `format_string` describes the type of the returned parameters. If the `command_function` does not return a value, the `format_string` is omirted. The dictionary with commands is used by the `UartRemote.wait_for_command()` method to call the function as defined upon receiving a specific command. As an argument the `data` that is received is used.
