from uartremote import *
u=UartRemote(Port.S1)


class Oled:
    def __init__(self,uartremote,width=128,height=64):
        self.uartremote=uartremote
        uartremote.send_receive("oledi","BB",width,height)

    def fill(self,color):
        self.uartremote.send_receive("oledf","B",color)
    
    def text(self,txt,x,y):
        s="%ds"%len(txt)
        return(self.uartremote.call("oledt",s+"BB",txt,x,y))

    def show(self):
        self.uartremote.send_receive("oleds")

oled=Oled(u)
oled.fill(0)
oled.text("This is cool!",0,10)
oled.show()

        
