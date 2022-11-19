from machine import I2C,Pin
from uartremote import *            # import UartRemote library

ur=UartRemote()
i2c=I2C(1,sda=Pin(5),scl=Pin(4))    # initialize I2C port as first hardware port
                                    # clock = Pin(4) and data = Pin(5)


def read_joy():
    q=i2c.readfrom(82,3)            # read 3 bytes from I2C sensor at address 82
    x=q[0]                          # x coordinate is first byte
    y=q[1]                          # y coordinate is 2nd byte
    button=q[2]                     # button pressed results in value 1 in the final byte
    return x,y,button

ur.add_command(read_joy,'repr')     # add the command 'read_joy' for use by the SPIKE Prime

ur.loop()                           # loop and wait for receiving 'read_joy' command