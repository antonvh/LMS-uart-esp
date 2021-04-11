from uartremote import *
u=UartRemote(port.A)


class Oled:
    def __init__(self,uartremote,width=128,height=64):
        self.uartremote=uartremote
        uartremote.send_receive("oledi","BB",width,height)

    def fill(self,color):
        self.uartremote.send_receive("oledf","B",color)
    
    def text(self,txt,x,y):
        self.uartremote.send_receive("oledt","sBB",txt,x,y)

    def line(self,x1,y1,x2,y2,color):
        self.uartremote.send_receive("oledl","5B",x1,y1,x2,y2,color)

    def pixel(self,x1,y1,color):
        self.uartremote.send_receive("oledp","3B",x1,y1,color)

    def show(self):
        self.uartremote.send_receive("oleds")

oled=Oled(u)
oled.fill(0)
oled.text("This is cool!",0,10)
oled.show()

        
