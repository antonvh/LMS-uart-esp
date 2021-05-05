from MP_ili9341 import ili9341
import machine
import time
import struct

from uartremote import *

machine.freq(160000000)


def bit24_to_bit16(colour):
    return  (colour[2] & 0xf8) << 8 | (colour[1] & 0xfc) << 3 | colour[0] >> 3      


class LCD:
    def __init__(self):
        self.screen = ili9341()

    def put_text(self,x,y,size,text,fg,bg):
        self.screen.put_text(x,y,size,text.decode('utf-8'),tuple(fg), tuple(bg))

    def fill_window(self,x,y,w,h,color):
        self.screen.set_window(x,y,w,h)
        n=w*h
        col16=struct.pack('>H',bit24_to_bit16(color))
        l=n
        w=1000
        while l > w:
            self.screen.send_spi(col16*w,True)
            l = l - w
        if l>0:
            self.screen.send_spi(col16*l,True)


u=UartRemote()
lcd=LCD()

u.add_command('text',lcd.put_text)
u.add_command('fill',lcd.fill_window)

u.loop()
