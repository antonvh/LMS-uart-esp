
import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S

i2c = I2C(scl=Pin(5), sda=Pin(4))
mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
sensor = MPU9250(i2c, mpu6500=mpu6500)

print("MPU9250 id: " + hex(sensor.whoami))

def imu(dummy):
    val=sensor.acceleration
    print("acc",val)
    return ('3f',val[0],val[1],val[2])


from uartremote import *

u=UartRemote(0)
u.add_command('imu',imu)
u.loop()