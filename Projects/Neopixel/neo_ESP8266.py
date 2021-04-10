import neopixel,machine

from uartremote import *

class Neo:
    def init(self,number_pixels,pin=machine.Pin(4)):
        self.np = neopixel.NeoPixel(pin, number_pixels)

    
    def setpixel(self,pix):
        # array of 4 values: [n,r,g,b]
        n=pix[0]
        (r,g,b)=pix[1:]
        self.np[n]=(r,g,b)
        #self.np.write()
    #return 'ok'

    def setpixelarray(self,pix):
        # array of m pixels starting form n [n,m,r1,g1,b1,...rm,gm,bm]
        n=pix[0]
        m=pix[1]
        for p in range(m):
            (r,g,b)=pix[2+3*p:5+3*p]
            self.np[p+n]=(r,g,b)

    def write(self):
        self.np.write()

u=UartRemote(0)
neo=Neo()
u.add_command('neoinit','',neo.init)
u.add_command('neos','',neo.setpixel)
u.add_command('neosa','',neo.setpixelarray)
u.add_command('neow','',neo.write)

u.loop()


'''
n=0
neo_init(8)
while True:
    q=neo_setpixel({'n':n%8,'c':(n%100,(n+50)%100,0)})
    q=neo_setpixel({'n':n%8,'c':(0,0,0)})
    n+=1
'''