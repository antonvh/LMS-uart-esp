import random
from neopixel import NeoPixel
from machine import Pin

np=NeoPixel(Pin(21),12)


def led(angle):
    led_nr=int(angle/(360/12))
    for i in range(12):
        np[i]=(0,0,0)
    np[led_nr]=(100,0,0)
    np.write()


def add_commands(ur):               # add this function to evenry module
                                    # you want to load and
                                    # define the commands you would like to
                                    # expose over the UartRemote connection
    ur.add_command(led)

