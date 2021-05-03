# Copy this script in a new Python project in the SPIKE Prima app to run it
# Upload uartremote.mpy to the esp breakout board using the webrepl.
# No need for a main.py. It is executed via the raw repl over serial.
# TO FIX; This program works for 30s or so and then the esp freezes.


MAINPY="""
from uartremote import *
from neopixel import NeoPixel
import utime
from math import sin

N_LEDS=12
ur = UartRemote()

offset = 0
def set_rotation(r):
    global offset
    offset = -r/360*150

color = (255,0,0)
def set_color(c):
    global color
    color = c

fps= 0
def get_fps():
    return fps

ur.add_command(get_fps,'f')
ur.add_command(set_rotation)
ur.add_command(set_color)

def init_pixels(length, pin=4):
    global np
    np = NeoPixel(machine.Pin(pin), length)

def hsl_to_rgb(h,s,l):
    c = (1 - abs(2*l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c/2
    r=g=b=int(m*255)
    xx = int((x+m)*255)
    cc = int((c+m)*255)
    if h < 60 or h > 300:
        r=cc
    if 60<=h<120 or 240<=h<300:
        r=xx
    if h<60 or 180<=h<240:
        g=xx
    if 60<=h<180:
        g=cc
    if 120<=h<180 or h>=300:
        b=xx
    if 180<=h<300:
        b=cc
    return (r,g,b)

def gauss1(x):
    # If x is in range (0, 100) return a number between 0 and 0.5
    # According to a guassian distribution
    # This gives us a smooth gradient on the leds. Guassian blur.
    x = x*6/100-3
    e=2.718281828459
    sqrt2pi_inv = 1/(3.1415*2)**0.5
    normal = sqrt2pi_inv*e**(-0.5*x**2)
    return normal * 1.25

def swirl(r_speed=-0.1, h_speed = 0.01):
    global np, offset
    offset = 0
    pix_pulse = 0
    led_indexes = list(range(N_LEDS))
    hue = 0.5
    while True:
        # Calculate lightnesses with a nice gaussian distribution
        lightnesses = [(gauss1((i*150/N_LEDS+offset)%150)+0.005)*(sin(pix_pulse)/3+0.8) for i in led_indexes]
        # Calculate rgb value with the current hue
        leds = [hsl_to_rgb(hue,1,l) for l in lightnesses]

        # Create a flat list of all color values in GRB format to write into the pixel buffer
        grb_flat = []
        for (r,g,b) in leds:
            grb_flat += [g,r,b]
        # write the complete neopixel buffer at once
        np.buf = bytearray(grb_flat)
        np.write()

        yield

        # increase rotation of image
        # offset += r_speed
        pix_pulse += 0.05

        # shift hue of 'image'
        hue += h_speed
        if hue > 360: hue = 0

def rotate():
    global np
    for i in range(12):
        np[i]=color
        yield
    for i in range(12):
        np[i]=(0,0,0)
        yield

swirlframe = swirl()
rotateframe = rotate()


def loop():
    global fps
    init_pixels(N_LEDS)
    ur.disable_repl_locally()
    while True:
        next(rotateframe)
        start = utime.ticks_ms()
        for i in range(100):
           try:
               next(swirlframe)
               if ur.available():
                    ur.execute_command(wait=False)
           except KeyboardInterrupt:
               self.enable_repl_locally()
               raise
           except:
               self.flush()
        duration = utime.ticks_diff(utime.ticks_ms(), start)
        fps = 100/duration*1000

# loop()
"""

from projects.uartremote import *

ur = UartRemote('F')

print("Uart initialized")

ur.repl_activate()
print(ur.repl_run("print('Repl Tested')"))
print(ur.repl_run(MAINPY))
print("loaded script")
ur.repl_run("loop()", reply=False)
print("entered loop")

ur.flush()
print("Flushed")


while True:
    r = hub.port.E.motor.get()[2]+130
    ur.call('set_rotation', 'i', int(r))
    print(ur.call('get_fps'))


raise SystemExit