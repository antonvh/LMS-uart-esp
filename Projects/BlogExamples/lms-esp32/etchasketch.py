from machine import Pin
from neopixel import NeoPixel
import time
from uartremote import *

neop=NeoPixel(Pin(21),64)
print("module loaded")

def led_xy(x,y,col):
    iy=y%8
    neop[iy*8+x]=col


neop=NeoPixel(Pin(21),64)    

def clear():
    for i in range(8):
        for j in range(8):
            led_xy(i,j,(0,0,0))
    neo.write()
    
def plotxy(x,y,r,g,b):
    led_xy(x,y,(r,g,b))
    neop.write()

def add_commands(ur):
    ur.add_command(clear) 
    ur.add_command(plotxy) 

