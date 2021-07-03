# LEGO MINDSTORMS Uart API libraries and breakout boards

## Hi there!

Welcom to this repository. If you just obtained one of the boards below, head over to the [Breakout Wiki](https://github.com/antonvh/LMS-uart-esp/wiki) to start soldering. All boards come pre-flashed so you shouldn't have to flash them. 

Once you're done soldering, head back here to try the libraries and example projects.


## [Libraries](https://github.com/antonvh/LMS-uart-esp/tree/main/Libraries)
We have built a couple of generic communication libraries allowing for easy communication between the MINDSTORMS hubs and other electronics.

### UartRemote
This library helps you to exchange data between two programs, if they have a serial communications link between them. Currently it is only implemented on UART links, but sockets and RFCOMM are serial links too. They should also benefit from this easy UART API. 

### LPF2
This library emulates power function motors and sensors over the UART protocol. This means you can integrate those sensor with minimal programming on the LEGO hub side.

## [Projects](https://github.com/antonvh/LMS-uart-esp/tree/main/Projects)
Example projects where we expand the EV3, SPIKE Prime and Robot Inventor hubs with third party electronics and hardware. Full code and instructions included as much as possible. 

## Work in Progress

In this folder you will find projects that we are currently working at. They will not necessarily be without bugs and they can be in an unfinished state. As soon as they are ready to execute, the projects will be moved to the Projects folder.
