# Before you can run this, you need to install mpy-robot-tools
# Run this script once in the MINDSTORMS app to install: https://github.com/antonvh/mpy-robot-tools/blob/master/Installer/install_mpy_robot_tools.py
# Be patient when it runs!


from mindstorms import Motor
from projects.mpy_robot_tools.uartremote import *
from time import sleep_ms
import time

class Oled:
    def __init__(self,uartremote,width=128,height=64):
        self.uartremote=uartremote
        uartremote.call("oledi","BB",width,height)

    def fill(self,color):
        return(self.uartremote.call("oledf","B",color))

    def text(self,txt,x,y):
        s="%ds"%len(txt)
        return(self.uartremote.call("oledt",s+"BB",txt,x,y))

    def line(self,x1,y1,x2,y2,color):
        self.uartremote.call("oledl","5B",x1,y1,x2,y2,color)

    def pixel(self,x1,y1,color):
        self.uartremote.call("oledp","3B",x1,y1,color)

    def show(self):
        return(self.uartremote.call("oleds"))


ur=UartRemote("B") # connect ESP to port A

ur.flush() # remove everything from rx buffer

print(ur.call('echo','repr',"Echo test is working"))
oled=Oled(ur)
# scroll text
for i in range(40):
    oled.fill(0)
    oled.text("This is cool!",10,i+5)
    oled.show()