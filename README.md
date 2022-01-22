# Anton's MINDSTORMS Hacks Breakout board - libraries and API

## Hi there!

Welcom to this repository. If you just obtained one of [our breakout boards](https://antonsmindstorms.com/product-category/electronics/), head over to the [Breakout Wiki](https://github.com/antonvh/LMS-uart-esp/wiki) to start soldering. All boards come pre-flashed so you shouldn't have to flash them. 

Once you're done soldering, head back here to try the libraries and example projects!

# Libraries/API

We have built a couple of generic communication libraries allowing for easy communication between the MINDSTORMS hubs and other electronics.


 - [UartRemote](https://github.com/antonvh/UartRemote)
This library helps you to exchange data between two programs, if they have a serial communications link between them. Currently it is only implemented on UART links, but sockets and RFCOMM are serial links too. They should also benefit from this easy UART API.
    - [LEGO Spike/51515 Hub](https://github.com/antonvh/UartRemote/tree/master/MicroPython/SPIKE)
    - [LEGO EV3](https://github.com/antonvh/UartRemote/tree/master/MicroPython/EV3)
    - [ESP8266](https://github.com/antonvh/UartRemote/tree/master/MicroPython/ESP8266)
    - [OpenMV](https://github.com/antonvh/UartRemote/tree/master/MicroPython/H7)
    - [Aduino](https://github.com/antonvh/UartRemote/tree/master/Arduino/UartRemote)

 -  [LPF2](https://github.com/antonvh/LMS-uart-esp/tree/main/Libraries/LPF2)
This library emulates power function motors and sensors over the UART protocol. This means you can integrate those sensor with minimal programming on the LEGO hub side. the [Distance Sensor Breakout board](https://antonsmindstorms.com/product/distance-sensor-breakout-board-for-spike-prime-and-robot-inventor/) would be an example.
     - [LPF2 Example](https://github.com/antonvh/LMS-uart-esp/tree/main/Libraries/LPF2/LPF2_simple) micropython, possible use case OpenMV is quickly connected with this example and can exchange digits 0-9 with the Lego Hub with minimal code.

 - [VL53](https://github.com/antonvh/LMS-uart-esp/tree/main/Libraries/vl53%20tof%20rangefinder)
This library is for use of the I2C VL53 chip, that can detect the "time of flight", or how long the light has taken to bounce back to the sensor for distance. Calibration and sensor readings.

 - [Huskylens](https://github.com/antonvh/LEGO-HuskyLenslib)
 Connect LEGO robots to the [Huskylens](https://wiki.dfrobot.com/HUSKYLENS_V1.0_SKU_SEN0305_SEN0336)
 
# Projects and Examples

 - [Example Projects](https://github.com/antonvh/LMS-uart-esp/tree/main/Projects) where we expand the EV3, SPIKE Prime and Robot Inventor hubs with third party electronics and hardware. Full code and instructions included as much as possible. 

 - [Work in Progress](https://github.com/antonvh/LMS-uart-esp/tree/main/WorkInProgress)
    In this folder you will find projects that we are currently working at. They will not necessarily be without bugs and they can be in an unfinished state. As soon as they are ready to execute, the projects will be moved to the Projects folder.
