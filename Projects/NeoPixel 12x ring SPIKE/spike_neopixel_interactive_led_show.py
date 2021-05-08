# Copy this script in a new Python project in the SPIKE Prima app to run it

# First, Install uartremote on the SPIKE with the installer script here:
# /Libraries/UartRemote/MicroPython/SPIKE/install_uartremote_mpy.py

# On the ESP/breakout Upload uartremote.mpy using the webrepl (see wiki).
# No need for a main.py. It is executed via the raw repl over serial.

# Typical output of this program:
# [10:45:27.797] > Uart initialized
# [10:45:28.461] > Repl tested
# [10:45:28.607] > None
# [10:45:28.636] > loaded script
# [10:45:28.687] > Entered remote command processing loop
# [10:45:28.759] > ('init_pixelsack', 'ok')
# [10:45:28.779] > Running light
# [10:45:44.468] > Running light, with lightness according to motor position
# [10:46:00.519] > Running light, with lightness according to motor position, and hue to another wheel
# [10:46:22.168] > Running light, with lightness according to motor position, and hue to another wheel, tighter beam
# [10:46:44.135] > Running light, with lightness according to motor position, and hue just shifting
# [10:47:05.867] > Running light, with lightness according to motor position, and hue rotation with other motor
# [10:47:28.408] > Running light, with lightness according to motor position, and hue rotation speed with other motor

MAINPY="""
from uartremote import *
from neopixel import NeoPixel

ur = UartRemote()

def init_pixels(length, pin=4):
    global np
    np = NeoPixel(machine.Pin(pin), length)

def set_pixel(n, color):
    global np
    np[n]=color

def paint():
    np.write()

def paint_buffer(bgr_bytes):
    global np
    np.buf=bytearray(bgr_bytes)
    np.write()

def paint_colors(*colors):
    global np
    for i in range(len(colors)):
        np[i] = colors[i]
    np.write()

ur.add_command(init_pixels)
ur.add_command(paint)
ur.add_command(set_pixel)
ur.add_command(paint_buffer)
ur.add_command(paint_colors)
"""

from projects.uartremote import *
from hub import port
from math import sin
import utime

ur = UartRemote('F')
print("Uart initialized")

ur.repl_activate()
print(ur.repl_run("print('Repl tested')"))
print(ur.repl_run(MAINPY))
print("loaded script")

N_LEDS = 12
N_UPDATES = 500
OFF = b'\x00\x00\x00'*N_LEDS

ur.repl_run("ur.loop()", reply=False)
print("Entered remote command processing loop")
print(ur.call('init_pixels','B',N_LEDS))

print("Running light")
for n in range(N_UPDATES):
    i = n % N_LEDS
    buf = i*b'\x00\x00\x00' + bytes((0,255,255)) + (N_LEDS-i-1)*b'\x00\x00\x00'
    ur.call('paint_buffer','raw',buf)

ur.call('paint_buffer','raw',OFF)
utime.sleep_ms(1000)

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

print("Running light, with lightness according to motor position")
twopi = 2*3.1415
for n in range(N_UPDATES):
    abs_pos = (port.E.motor.get()[2]%360+180)/-360*twopi
    i = n % N_LEDS
    lightness = 0.3 * (sin(twopi/N_LEDS*i + abs_pos)+1)
    # print(lightness)
    buf = i*b'\x00\x00\x00' + bytes(hsl_to_rgb(0,1,lightness)) + (N_LEDS-i-1)*b'\x00\x00\x00'
    ur.call('paint_buffer','raw',buf)

ur.call('paint_buffer','raw',OFF)
utime.sleep_ms(1000)

print("Running light, with lightness according to motor position, and hue to another wheel")
for n in range(N_UPDATES):
    abs_pos = (port.E.motor.get()[2]%360+170)/-360*twopi
    hue = port.A.motor.get()[2]%360
    buf=b''
    for i in range(N_LEDS):
        lightness = 0.2 * (sin(twopi/N_LEDS*i + abs_pos)+1)
        # print(lightness)
        buf += bytes(hsl_to_rgb(hue,1,lightness))
    ur.call('paint_buffer','raw',buf)

ur.call('paint_buffer','raw',OFF)
utime.sleep_ms(1000)

print("Running light, with lightness according to motor position, and hue to another wheel, tighter beam")
for n in range(N_UPDATES):
    abs_pos = (port.E.motor.get()[2]%360+170)/-360*twopi
    hue = port.A.motor.get()[2]%360
    buf=b''
    for i in range(N_LEDS):
        lightness = 0.4 * max(sin(twopi/N_LEDS*i + abs_pos)+0.5, 0)
        # print(lightness)
        buf += bytes(hsl_to_rgb(hue,1,lightness))
    ur.call('paint_buffer','raw',buf)

ur.call('paint_buffer','raw',OFF)
utime.sleep_ms(1000)

print("Running light, with lightness according to motor position, and hue just shifting")
for n in range(N_UPDATES):
    abs_pos = (port.E.motor.get()[2]%360+170)/-360*twopi
    hue = n%360
    buf=b''
    for i in range(N_LEDS):
        lightness = 0.3 * max(sin(twopi/N_LEDS*i + abs_pos)+1, 0)
        # print(lightness)
        buf += bytes(hsl_to_rgb(hue,1,lightness))
    ur.call('paint_buffer','raw',buf)

ur.call('paint_buffer','raw',OFF)
utime.sleep_ms(1000)

print("Running light, with lightness according to motor position, and hue rotation with other motor")
for n in range(N_UPDATES):
    abs_pos = (port.E.motor.get()[2]%360+170)/-360*twopi
    hue_offset = port.A.motor.get()[2]%360
    buf=b''
    for i in range(N_LEDS):
        lightness = 0.3 * max(sin(twopi/N_LEDS*i + abs_pos)+1, 0)
        hue = (360*i/12 + hue_offset)%360
        # print(lightness)
        buf += bytes(hsl_to_rgb(hue,1,lightness))
    ur.call('paint_buffer','raw',buf)

ur.call('paint_buffer','raw',OFF)
utime.sleep_ms(1000)

print("Running light, with lightness according to motor position, and hue rotation speed with other motor")
hue_offset = 0
for n in range(N_UPDATES):
    abs_pos = (port.E.motor.get()[2]%360+170)/-360*twopi
    hue_offset_inc = port.A.motor.get()[2]//7
    hue_offset += hue_offset_inc
    buf=b''
    for i in range(N_LEDS):
        lightness = 0.3 * max(sin(twopi/N_LEDS*i + abs_pos)+1, 0)
        hue = (360*i/12 + hue_offset)%360
        # print(lightness)
        buf += bytes(hsl_to_rgb(hue,1,lightness))
    ur.call('paint_buffer','raw',buf)

ur.call('paint_buffer','raw',OFF)
utime.sleep_ms(1000)

print("Running light, with hue according to motor position, and pulse speed with other motor")
pulse = 0
for n in range(N_UPDATES):
    hue_offset = (-port.E.motor.get()[2]+170)%360
    pulse_speed = port.A.motor.get()[1]//7
    pulse += pulse_speed/50
    buf=b''
    for i in range(N_LEDS):
        lightness = 0.2 + 0.1 * max(sin(pulse)+1, 0)
        hue = (360*i/12 + hue_offset)%360
        # print(lightness)
        buf += bytes(hsl_to_rgb(hue,1,lightness))
    ur.call('paint_buffer','raw',buf)

raise SystemExit