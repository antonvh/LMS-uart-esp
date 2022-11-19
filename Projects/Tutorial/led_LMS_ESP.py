from uartremote import *            # import UartRemote library
import random   
from neopixel import NeoPixel       # import NeoPixel library       
from machine import Pin

ur=UartRemote()
np=NeoPixel(Pin(21),12)             # 12 led neopixel is connected to Pin(21)


def led(angle):
    led_nr=int(angle/(360/12))      # calculate led corresponsing to angle
    for i in range(12):
        np[i]=(0,0,0)               # switch all leds off
    np[led_nr]=(100,0,0)            # set led corresponding with angle to 'red'=(100,0,0)
    np.write()                      # write values to NeoPixel
    
ur.add_command(led)                 # add the command 'led' for usage by the SPIKE PRIME

ur.loop()                           # wait for the 'led' command to be received