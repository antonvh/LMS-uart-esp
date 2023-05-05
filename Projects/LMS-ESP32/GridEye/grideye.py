from machine import Pin,I2C
import machine
import utime
from amg88xx import AMG88XX
import time
from ulab import numpy as np
from neopixel import NeoPixel
import math
from uartremote import *

ur=UartRemote()

neo=NeoPixel(Pin(23),64)

i2c = machine.I2C(1,sda=Pin(22),scl=Pin(21),freq=400000)
sensor = AMG88XX(i2c,addr=104)
sensor.ma_mode(False)

def zero():
    for i in range(64):
        neo[i]=(0,0,0)
    neo.write()

from math import sin, pi

def clamp(value, min_value, max_value):
    return max(min_value, min(max_value, value))

def saturate(value):
    return clamp(value, 0.0, 1.0)

def hue_to_rgb(h):
    r = abs(h * 6.0 - 3.0) - 1.0
    g = 2.0 - abs(h * 6.0 - 2.0)
    b = 2.0 - abs(h * 6.0 - 4.0)
    return saturate(r), saturate(g), saturate(b)

def hsl_to_rgb(h, s, l):
    # Takes hue in range 0-359, 
    # Saturation and lightness in range 0-99
    h /= 359
    s /= 100
    l /= 100
    r, g, b = hue_to_rgb(h)
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    r = (r - 0.5) * c + l
    g = (g - 0.5) * c + l
    b = (b - 0.5) * c + l
    rgb = tuple([round(x*255) for x in (r,g,b)])
    return rgb


def color(t):
    tt=t-20
    if tt>0:
        r=tt*2
    else:
        r=0
    g=(25-t)
    if g<0:
        g=0
    return(int(r),int(g),0)


def get_grid():
    global grid
    sensor.refresh()
    q=np.frombuffer(sensor._buf,dtype=np.int16)/4.
    #q=q[::-1]
    grid=q.reshape((8,8))
    grid=np.array([[grid[j][i] for j in range(8)] for i in range(8)])
    #grid=grid[::-1]
    #if max(q)>(sum(q)/64)+3:
    #print(sum(q)/64,max(q),time.ticks_ms())
    #return grid
    
def show_grid():
    q=grid.flatten()
    for i in range(len(q)):
        #neo[i]=hsl_to_rgb((180+(q[i]-16)*10)%360,80,int(q[i]//6)*2)
        neo[i]=color(q[i])
    neo.write()
    
    
def get_pos():
    get_grid()
    show_grid()
    m=np.max(grid)
    n=np.argmax(grid)
    mx=n//8
    my=n%8
    avg=np.sum(grid)/64
    return (m,avg,mx,my)


ur.add_command(get_pos,'2f2B')

ur.loop()