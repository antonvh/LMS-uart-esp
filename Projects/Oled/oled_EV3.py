from uartfast import *
u=UartRemote(Port.S1)


class Oled:
    def __init__(self,uartremote,width=128,height=64):
        self.uartremote=uartremote
        uartremote.send_receive("oledi","BB",width,height)

    def fill(self,color):
        self.uartremote.send_receive("oledf","B",color)
    
    def text(self,txt,x,y):
        f="%dsBB"%len(txt)    # format string for string and 2 unsigned bytes
        self.uartremote.send_receive("oledt",f,txt,x,y)

    def show(self):
        self.uartremote.send_receive("oleds")

oled=Oled(u)
oled.fill(0)
oled.text("This is cool!",0,10)
oled.show()

        
