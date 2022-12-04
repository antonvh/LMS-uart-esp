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
        s="%ds"%len(txt)
        return(self.uartremote.call("oledt",s+"BB",txt,x,y))

    def line(self,x1,y1,x2,y2,color):
        self.uartremote.call("oledl","5B",x1,y1,x2,y2,color)

    def pixel(self,x1,y1,color):
        self.uartremote.call("oledp","3B",x1,y1,color)

    def show(self):
        return(self.uartremote.call("oleds"))


ur=UartRemote("E") # connect ESP to port A

ur.flush() # remove everything from rx buffer

ur.repl_activate()
print(ur.repl_run("print('Repl Tested')")) # check remote repl
ur.repl_run(RESET,reply=False) # to re-load library, soft reset is needed
sleep_ms(200)
ur.repl_activate()
ur.repl_run(MAINPY,reply=False)

# Sleep is needed for the uart to stablize???
sleep_ms(1000)

print(ur.call('echo','repr',"Echo test is working"))
oled=Oled(ur)
# scroll text
for i in range(40):
    oled.fill(0)
    oled.text("This is cool!",10,i+5)
    oled.show()
