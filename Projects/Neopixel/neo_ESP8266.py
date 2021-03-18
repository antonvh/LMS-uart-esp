import neopixel,machine

from uartremote import *

np=[]

def neo_init(number_pixels,pin=machine.Pin(4)):
    global np
    np = neopixel.NeoPixel(pin, number_pixels)
    return 'ok'

def neo_setpixel(pix):
    global np
    n=pix['n']
    (r,g,b)=pix['c']
    np[n]=(r,g,b)
    np.write()
    return 'ok'

u=UartRemote(0)
u.add_command('neo',neo_init)
u.add_command('neo_set',neo_setpixel)
u.loop()
