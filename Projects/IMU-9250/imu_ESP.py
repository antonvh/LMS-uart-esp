# library https://github.com/tuupola/micropython-mpu9250
# single change for different WHOAMI value for MPU-892/65board
# line 97 of mpu6500.py, 0x73 added
#     if self.whoami not in [0x73,0x71, 0x70]:
    


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


from uartfast import *

u=UartRemote(0)
u.add_command('acc',acc)
u.loop()