from machine import I2C,Pin
from uartremote import *

ur=UartRemote()
i2c=I2C(1,sda=Pin(5),scl=Pin(4))


def read_joy():
    q=i2c.readfrom(82,3)
    x=q[0]
    y=q[1]
    button=q[2]
    return x,y,button

ur.add_command(read_joy,'repr')

ur.loop()