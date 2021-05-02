from spike import Motor
from projects.uartremote import *
from time import sleep_ms
import time

RESET="""
import machine
machine.soft_reset()
"""

MAINPY="""
from oled_ESP import *
"""

class Oled:
    def __init__(self,uartremote,width=128,height=64):
        self.uartremote=uartremote
        uartremote.call("oledi","BB",width,height)

    def fill(self,color):
        return(self.uartremote.call("oledf","B",color))

    def text(self,txt,x,y):
        return(self.uartremote.call("oledt","sBB",txt,x,y))

    def line(self,x1,y1,x2,y2,color):
        self.uartremote.call("oledl","5B",x1,y1,x2,y2,color)

    def pixel(self,x1,y1,color):
        self.uartremote.call("oledp","3B",x1,y1,color)

    def show(self):
        return(self.uartremote.call("oleds"))


ur=UartRemote("A") # connect ESP to port A

ur.flush() # remove everything from rx buffer

ur.repl_activate()
print(ur.repl_run("print('Repl Tested')")) # check remote repl 
ur.repl_run(RESET,reply=False) # to re-load library, soft reset is needed 
ur.repl_activate()
ur.repl_run(MAINPY,reply=False)

# Sleep is needed for the uart to stablize???
time.sleep_ms(500)

print(ur.call('echo','s',"Echo test is working"))
oled=Oled(ur)
# scroll text
for i in range(40):
    oled.fill(0)
    oled.text("This is cool!",10,i+5)
    oled.show()
