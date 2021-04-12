from spike import ColorSensor
from uartremote import *

u=UartRemote(port.A)

c=ColorSensor("B")

u.send_receive('neoinit',8)

def getcolor():
     r=c.get_red()>>3
     g=c.get_green()>>3
     b=c.get_blue()>>3
     return [r,g,b]

while True:
     q=u.send_receive('neosa','B',[0,8]+getcolor()*8)
     q=u.send_receive('neow')
