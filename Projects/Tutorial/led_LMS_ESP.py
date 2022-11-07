from uartremote import *
import random
from neopixel import NeoPixel
from machine import Pin

ur=UartRemote()
np=NeoPixel(Pin(21),12)


def led(angle):
    led_nr=int(angle/(360/12))
    for i in range(12):
        np[i]=(0,0,0)
    np[led_nr]=(100,0,0)
    np.write()
    
ur.add_command(led)

ur.loop()