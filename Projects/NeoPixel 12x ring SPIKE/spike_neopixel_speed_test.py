# Copy this script in a new Python project in the SPIKE Prima app to run it

# First, Install uartremote on the SPIKE with the installer script here:
# /Libraries/UartRemote/MicroPython/SPIKE/install_uartremote_mpy.py

# On the ESP/breakout Upload uartremote.mpy using the webrepl (see wiki).
# No need for a main.py. It is executed via the raw repl over serial.

# Note that this script increases the clock frequency of the esp to 160MHz!

# Typical output of this program:
# [10:29:45.294] > loaded script
# [10:29:47.823] > Paint with raw repl pixel set succeeded at 40.3714 updates per second.
# [10:29:47.847] > Entered remote command processing loop
# [10:29:47.915] > ('init_pixelsack', 'ok')
# [10:30:08.614] > Paint with 'B' color array succeeded at 4.83652 updates per second.
# [10:30:19.161] > Pixel setting & paint succeeded at 9.5347 updates per second.
# [10:30:24.112] > Direct buffer paint with 'r' succeeded at 20.3046 updates per second.
# [10:30:27.053] > Direct buffer paint with 'raw' succeeded at 34.2701 updates per second.

MAINPY="""
from uartremote import *
from neopixel import NeoPixel
machine.freq(160000000)

ur = UartRemote()
color = (255,0,255)

def init_pixels(length, pin=4):
    global np
    np = NeoPixel(machine.Pin(pin), length)

def set_pixel(n, color):
    global np
    np[n]=color

def set_color(color_update):
    global color
    color = color_update

def paint():
    np.write()

def paint_buffer(bgr_bytes):
    global np
    np.buf=bgr_bytes
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
import utime
ur = UartRemote('F')
print("Uart initialized")

ur.repl_activate()
print(ur.repl_run("print('Repl tested')"))
print(ur.repl_run(MAINPY))
print("loaded script")

N_LEDS = 12
N_UPDATES = 100

start = utime.ticks_ms()
ur.repl_run("np = NeoPixel(machine.Pin(4), {})".format(N_LEDS))
for n in range(N_UPDATES):
    i = n % N_LEDS
    ur.repl_run("""
np[{}] = (0,0,0)
np[{}] = (255,0,0)
np.write()
    """.format(i-1,i))
duration = utime.ticks_diff(utime.ticks_ms(), start)
print("Paint with raw repl pixel set succeeded at {} updates per second.".format(N_UPDATES/duration*1000))

ur.repl_run("ur.loop()", reply=False)
print("Entered remote command processing loop")

print(ur.call('init_pixels','B',N_LEDS))

start = utime.ticks_ms()
colors_off = N_LEDS * [(0,0,0)]
for n in range(N_UPDATES):
    i = n % N_LEDS
    colors = colors_off[:]
    colors[i] = (0,0,255)
    ur.call('paint_colors', N_LEDS*'B',*colors)
duration = utime.ticks_diff(utime.ticks_ms(), start)
print("Paint with 'B' color array succeeded at {} updates per second.".format(N_UPDATES/duration*1000))

start = utime.ticks_ms()
for n in range(N_UPDATES):
    i = n % N_LEDS
    ur.call('set_pixel','bB',i-1,[0,0,0])
    ur.call('set_pixel','bB',i,[255,0,255])
    ur.call('paint')
duration = utime.ticks_diff(utime.ticks_ms(), start)
print("Pixel setting & paint succeeded at {} updates per second.".format(N_UPDATES/duration*1000))

start = utime.ticks_ms()
for n in range(N_UPDATES):
    i = n % N_LEDS
    buf = i*b'\x00\x00\x00' + bytes((255,0,255)) + (N_LEDS-i-1)*b'\x00\x00\x00'
    ur.call('paint_buffer','r',buf)
duration = utime.ticks_diff(utime.ticks_ms(), start)
print("Direct buffer paint with 'r' succeeded at {} updates per second.".format(N_UPDATES/duration*1000))

start = utime.ticks_ms()
for n in range(N_UPDATES):
    i = n % N_LEDS
    buf = i*b'\x00\x00\x00' + bytes((0,255,255)) + (N_LEDS-i-1)*b'\x00\x00\x00'
    ur.call('paint_buffer','raw',buf)
duration = utime.ticks_diff(utime.ticks_ms(), start)
print("Direct buffer paint with 'raw' succeeded at {} updates per second.".format(N_UPDATES/duration*1000))

raise SystemExit