from machine import I2C,Pin
from uartremote import *
from vl53 import *             # include VL53 sensor library

u=UartRemote()                 # initailize UartRemote

# initialize I2C interface nr. 1
i2c=I2C(1,scl=Pin(4),sda=Pin(5))
tof=VL53L0X(i2c)                # init VL53 sensor
tof.start()                     # start VL54 sensor

def vl53():
  d=tof.read()
  return d 
  
u.add_command(vl53,'i')         # add vl53 function to commands
 
u.loop()                        # wait for a command to be executed