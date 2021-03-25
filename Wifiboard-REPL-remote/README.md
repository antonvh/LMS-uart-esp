# WifiBoard (pyboard) REPL Remote

This is a simple library intended to be copied in Python SPIKE Prime or Python MINDSTORMS Robot Inventor projects. It allows you to exectute MicroPython code remotely on the Wifiboard and get the results. Unlike the Uart lib, this doesn't require any software to run on the wifi-board. 

The code is based on the pyboard tool from Micropython and uses RAW REPL.

## Usage
```
# Driving an IO Pin
wifi = WifiBoard('C') # Port C in the SPIKE or RI hub.
wifi.enter_raw_repl()
wifi.execute("from machine import Pin")
wifi.execute("p4 = Pin(4, Pin.OUT)")
wifi.execute("p4.value(1)")

# Getting a value back (as string)
result = wifi.execute("print(5**2)")
print(result) # prints "25".
```

## Example applications
- Simple LED (Neopixel) projects
- Simple projects that require just driving an IO pin. Like [switching a relais](../Projects/Relais EV3)