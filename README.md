# LMS-uart-esp

This repository contains code from SPIKE Prime I2C and OpenMV hacking experiments.

Be sure to also check out the [Wiki](https://github.com/antonvh/LMS-uart-esp/wiki) to get started with soledering, flashing and set-up.

## LMS-uart lib
Handy classes to help you to transfer data from the WifiBoard esp to your MINDSTORMS hub and vice versa. A very lightweight RPC. Requires a main.py running on the wifiboard to respond to data requests and procedure calls. Runs up to 20 calls per second.

## WifiBoard REPL Remote
Easily execute MicroPython commands on the remote board. No software needed on the remote board. Prototype the calls via the WebREPL and the build them into your MINDSTORMS script with this library.

## Projects
Example projects where we expand the EV3, SPIKE Prime and Robot Inventor hubs with third party electronics and hardware. Full code and instructions included as much as possible. 