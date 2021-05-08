# Copy this script in a new Python project in the SPIKE Prima app to run it
# Upload uartremote.mpy to the esp breakout board using the webrepl.
# No need for a main.py. It is executed via the raw repl over serial.
# TO FIX; This program works for 30s or so and then the SPIKE freezes.
# It seems to get stuck in a ur.call() command.

MAINPY="""
from uartremote import *
from neopixel import NeoPixel
import utime
from math import sin

N_LEDS=12
ur = UartRemote()

fps= 0
def get_fps():
    global fps
    return fps

color = (255,0,0)
def set_color(hue):
    global color
    color = hsl_to_rgb(hue, 1.0, 0.5)

ur.add_command(get_fps,'f')
ur.add_command(set_color)

def init_pixels(length, pin=4):
    global np
    np = NeoPixel(machine.Pin(pin), length)

def hsl_to_rgb(h,s,l):
    # hue is between 0-359
    # saturation and lightness are between 0-1
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

def rotate():
    global np
    while True:
        for i in range(12):
            # Update lit pixels in case the color has changed
            for j in range(i):
                np[j]=color

            # Now slowly turn the last pixel on.
            for c in range(255):
                np[i]=[min(x,c) for x in color]
                np.write()
                yield # Pause and check uart
        # Slowly turn them off again
        for i in range(12):
            # Update lit pixels in case the color has changed
            for j in range(i+1, 12):
                np[j]=color

            for c in range(255,-1,-1):
                np[i]=[min(x,c) for x in color]
                np.write()
                yield # Pause and check uart

rotateframe = rotate()

def loop():
    global fps
    init_pixels(N_LEDS)
    ur.disable_repl_locally()
    while True:
        start = utime.ticks_ms()
        for i in range(100):
            try:
                next(rotateframe)
                if ur.available():
                    ur.execute_command(wait=False)
            except KeyboardInterrupt:
                ur.enable_repl_locally()
                raise
            except:
                ur.flush()
        duration = utime.ticks_diff(utime.ticks_ms(), start)
        fps = 100/duration*1000

# Don't loop just yet...
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

while True:
    r = hub.port.E.motor.get()[2]%360
    ur.call('set_color', 'i', r)
    ack, fps = ur.call('get_fps')
    print("Running at {}fps on the ESP breakout".format(fps))

raise SystemExit