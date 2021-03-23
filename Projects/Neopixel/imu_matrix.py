import neopixel,machine
import utime
from machine import I2C, Pin
from mpu9250 import MPU9250
from mpu6500 import MPU6500, SF_G, SF_DEG_S


from uartfast import *

class Neo:
    def neo_init(self,number_pixels,pin=machine.Pin(13)):
        self.np = neopixel.NeoPixel(pin, number_pixels[0])

    def neo_setpixel(self,pix):
        n=pix[0]
        (r,g,b)=pix[1:]
        self.np[n]=(r,g,b)
        self.np.write()
    #return 'ok'

i2c = I2C(scl=Pin(5), sda=Pin(4))
mpu6500 = MPU6500(i2c, accel_sf=SF_G, gyro_sf=SF_DEG_S)
sensor = MPU9250(i2c, mpu6500=mpu6500)

print("MPU9250 id: " + hex(sensor.whoami))

def acc():
    val=sensor.acceleration
    return ('f',[val[0],val[1],val[2]])


u=UartRemote(0)
u.add_command('acc',acc)
neo=Neo()
u.add_command('neo',neo.neo_init)
u.add_command('nes',neo.neo_setpixel)

u.loop()