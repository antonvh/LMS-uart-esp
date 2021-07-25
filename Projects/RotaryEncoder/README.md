# Rotary Encoder
This is a project for building a frictionless rotary encoder with 20 steps per revolution. By using some gear transmission, the precision can be increased. These encoders can be used for frictionless odometry by driving them by e.g. omni wheels.


![Magentic encoder mounted in lego](./images/magentic_encoder_lego.jpg)

## Example code

Upload the file `rotary.py` to the ESP8266 board using WebREPL. Copy the program `rotarySPIKE.py` in a new python project for Spike Prime or Mindstorms Robot inventor. The UartRemote library should already be installed on both the ESP8266 and the robot brick. Connect a motor to port B, connect the ESP8266 module to port A. The motor should follow the rotation of the encoder.

## Hardware
This example allows you tpo connect a rotary encoder to two digital pins of the ESP8266 Board. In this example we use GPIO4 and GPIO5, which are labeled on the ESP8266 baord as `SDA`, and `SCL`, respectively. These bits will be called `A` and `B` in the remainder of this write up.


We use a magnetic encoder designed by polulo (see (https://www.pololu.com/product/3499)). This encoder uses high-precision Hall effect sensors to probe changes of orientation of a 10-pole magnetic disk.

## 3D printed lego mounts

I designed a holder for the magnet that can be attached to a lego axle, and a mount for the magnetic encoder pcb. The STL-files can be found on [thingiverse](https://www.thingiverse.com/thing:4913776).  Use a axle with a thin flange in the middle hole to keep the encoder fixed in the mount.

## Background
The MicroPython code used in this projects lives on Github: [MicrPython Rotary](https://github.com/miketeachman/micropython-rotary). However, this projects decodes only half steps, whereas the rotary sensor could be decoded using quadrature decoding, giving a step at each transistion.

### State diagram
When turning clockwise (CW), the following consecutive bit states (`AB`) are observed: `00 -> 10 -> 11 -> 01 -> 00 ...`. Turning counter clockwise (CCW), the states are visited in the opposite order: `00 -> 01 -> 11 -> 10 -> 00 ...`.
From that the following state diagram can be drawn:
|state | `00` | `01` | `10` | `11` |
|------|------|------|------|------|
|`00` | 0 | -  | + | 0|
|`01` | + | 0  | 0 | -|
|`10` | - | 0  | 0 | +|
|`11` | 0 | +  | - | 0|

where '+' indicates a CW step and '-' indicates a CCW step.

### Quadrature algorithm
If we set at start a counter to 0, the following loop will count the steps in CW and CCW and adjust the counter accordingly

```python
import time

states=[
	[0,-1,1,0],
	[1,0,0,-1],
	[-1,0,0,1],
	[0,1,-1,0]
]

old_state=(r._get_bit_A() <<1) | r._get_bit_B()
counter=0
while True:
    new_state=(r._get_bit_A() <<1) | r._get_bit_B()
    if old_state!=new_state:
        counter+=states[old_state][new_state]
        print(old_state,state,states[old_state][new_state],counter)
        old_state=new_state
    time.sleep_ms(10) # give some time
```

