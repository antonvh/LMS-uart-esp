
from uartremote import *

u=UartRemote(Port.S1)

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


q=[[0,0]]
l=0
neo=Neo(u,64)

x=4
y=4
while True:
    #neo.set_pixel((x*8+y)%64,0,0,0)
    (resp,value)=u.send_receive('acc')
    x=7-int(value[0]*4+4)
    y=7-int(value[1]*4+4)
    p=(x*8+y)%64
    if p!=q[-1][0]:
        q.append([p,100])
        l=len(q)
        if l>10:
        q=q[1:]
        q[0]=[q[0][0],0]
        print("======")
        for i in range(len(q)):
            print(q[i][0],q[i][1])
            neo.set_pixel(q[i][0],q[i][1],0,0)
            if i>0:
            q[i]=[q[i][0],int(q[i][1]*0.7)]
        
    
    
    
