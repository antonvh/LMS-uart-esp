import neopixel,machine

from uartfast import *

class Neo:
    def neo_init(self,number_pixels,pin=machine.Pin(13)):
        self.np = neopixel.NeoPixel(pin, number_pixels[0])

    def neo_setpixel(self,pix):
        n=pix[0]
        (r,g,b)=pix[1:]
        self.np[n]=(r,g,b)
        self.np.write()
    #return 'ok'

u=UartRemote(0)
neo=Neo()
u.add_command('neo',neo.neo_init)
u.add_command('nes',neo.neo_setpixel)

u.loop()


'''
n=0
neo_init(8)
while True:
    q=neo_setpixel({'n':n%8,'c':(n%100,(n+50)%100,0)})
    q=neo_setpixel({'n':n%8,'c':(0,0,0)})
    n+=1
'''