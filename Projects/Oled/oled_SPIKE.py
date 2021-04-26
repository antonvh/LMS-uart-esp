from spike import Motor
from projects.uartremote import *
from time import sleep_ms
import time

MAINPY="""
from oled_ESP import *
"""

ur=UartRemote("A") # connect ESP to port A


ur.flush() # remove evernything
# try to enable repl if esp is still in non_repl mode
#ur.send_command("enable repl",'s','ok')
#print("response enable repl",ur.uart.read(100))

ur.repl_activate()
print(ur.repl_run("print('Repl Tested')"))
print(ur.repl_run(MAINPY,reply=False))
print(ur.uart.read(1024))
print("loaded script")



class Oled:
    def __init__(self,uartremote,width=128,height=64):
        self.uartremote=uartremote
        print(self.uartremote.encode("cmd",'f',1.234556))
        print(uartremote.call("oledi","BB",width,height))

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

# Sleep is needed for the uart to stablize???
print("before sleep")
time.sleep(1)
print("after sleep")
print(ur.call('echo','s','Werkt dit?'))


print("initialize oled")
oled=Oled(ur)
print("ready initializing oled")
print(oled.fill(0))
print(oled.text("This is cool!",0,10))
print(oled.show())
