# Remote UART library: uartremote.py

This is a library for robust communication between lego EV3/Spike and other MicroPython modules using the UART.

## Micropython

This is a uniform library that works on standard MicroPython platforms, the EV3 and the Spike. 

## Arduino

The same UartRemote library is also implemented for Arduino.
ontains `error`.

# packet format
When a command with its accompanying values is transmitted over the Uart, the following packet format is used:

|delimiter|total len|command len|command|format len| format| data|delimiter|
|---------|---------|-----------|-------|----------|-------|-----|---------|
| `\<`      |  `ln`   | `lc`    | `cmd` | `lf`    | `f` | binary data | `\>`|

with
- `ln` the length of the total packet encoded as a single byte,
- `lc` the length of the command string `<cmd>` as a single byte,
- `cmd` the command specified as a string,
- `lf` the length of the format string
- `f` the Format character used for `struct.pack` to pack the values; when data is a list, the character `a` is prepended to `f`.
- `data` a number of values packed using `struct.pack`

When the command
`send_receive('test','B',[1,2,3,4,5]`
is used, the following packet will be transmitted over the line:

```b'\x0e\x04test\x03a5B\x01\x02\x03\x04\x05'```

or in hex:

```0e0474657374036135420102030405```

When the Format string `f` is a single character, and the data is a list, each element of the list will be encoded using the specified Format character. The format field can also consist of multiple Format characters, for example 

```send_receive('special','3b3s1f',1,2,3,"aap",1.3)```.

