# MCU9250 example

The MCU9250 module consists of the MCU-6050 3 axis Gyro and accelerometer and the Ak8963 magnetic field meter.

This example uses the micropython libraries at https://github.com/tuupola/micropython-mpu9250

![mpu9250](https://github.com/antonvh/LMS-uart-esp/blob/main/Projects/IMU-9250/Images/mpu-9265.jpg)


## ESP8266

Install the libaries `mpu9250.py`, `mpu6500,py`, and `ak8963.py`. Furthermore, install the library `uartremote.py` that can be found in this repository. Upload the code `imu_ESP.py`.

```python
import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S

i2c = I2C(scl=Pin(5), sda=Pin(4))
mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
sensor = MPU9250(i2c, mpu6500=mpu6500)

print("MPU9250 id: " + hex(sensor.whoami))

def acc():
    val=sensor.acceleration
    return ('f',[val[0],val[1],val[2]])


from uartremote import *

u=UartRemote(0)
u.add_command('acc',acc)
u.loop()
```


## EV3

On the EV3 run the following code:

```python
from uartremote import *
u=Uartremote(Port.S1)

while True:
    print(u.send_receive('acc'))
```
