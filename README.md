# LMS-uart-esp

This repository contains code from SPIKE Prime I2C and OpenMV hacking experiments.

Be sure to also check out the [Wiki](https://github.com/antonvh/LMS-uart-esp/wiki) to get started with soledering, flashing and set-up.

## Libraries

Generic communication libraries allowing for easy communication between the MINDSTORMS hubs and the WifiBoard ESP.

### UartRemote
A very lightweight RPC. Requires a main.py running on the wifiboard to respond to data requests and procedure calls. Runs up to 20 calls per second.

### WifiBoard REPL Remote
Easily execute MicroPython commands on the remote board. No software needed on the remote board. Prototype the calls via the WebREPL and the build them into your MINDSTORMS script with this library.

## Projects
Example projects where we expand the EV3, SPIKE Prime and Robot Inventor hubs with third party electronics and hardware. Full code and instructions included as much as possible. 

## Work in Progress

In this folder you will find projects that we are currently working at. They will not necessarily be without bugs and they can be in an unfinished state. As soon as they are ready to execute, the projects will be moved to the Projects folder.