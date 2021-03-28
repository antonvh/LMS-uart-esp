from uartremote import *
from vl53 import *

u=UartRemote(0)

from machine import I2C,Pin
i2c=I2C(scl=Pin(5),sda=Pin(4))
tof=VL53L0X(i2c)    
tof.start()

def vl53():
  d=tof.read()
  return ('i',d) # return integer
  
u.add_command('vl53',vl53)
 
u.loop()