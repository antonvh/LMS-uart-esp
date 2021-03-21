from uartfast import *
u=UartRemote(Port.S1)
from time import sleep

class Neo:
    uart_remote=1
    
    def __init__(self,uart_remote,number_pixels):
        self.number_pixels=number_pixels
        self.uart_remote=uart_remote
        self.uart_remote.send_receive('neo','b',number_pixels)
    
    def set_pixel(self,pixel,r,g,b):
        self.uart_remote.send_receive('nes','b',[pixel,r,g,b])

    def off(self):
        for i in range(self.number_pixels):
            self.uart_remote.send_receive('nes','b',[i,0,0,0])



neo=Neo(u,8)

n=0
while True:
    neo.set_pixel(n%8,100,100,0)
    neo.set_pixel(n%8,0,0,0)
    n+=1

