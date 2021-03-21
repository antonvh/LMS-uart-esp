import neopixel,machine

from uartfastb import *

np=[]

def neo_init(number_pixels,pin=machine.Pin(4)):
    global np
    np = neopixel.NeoPixel(pin, number_pixels)
    #return 'ok'

def neo_setpixel(pix):
    global np
    n=pix[0]
    (r,g,b)=pix[1:]
    np[n]=(r,g,b)
    np.write()
    #return 'ok'

u=UartFast(0)
u.add_command('neo','rnr',neo_init)
u.add_command('nes','rns',neo_setpixel)
u.loop()


'''
n=0
neo_init(8)
while True:
    q=neo_setpixel({'n':n%8,'c':(n%100,(n+50)%100,0)})
    q=neo_setpixel({'n':n%8,'c':(0,0,0)})
    n+=1
'''