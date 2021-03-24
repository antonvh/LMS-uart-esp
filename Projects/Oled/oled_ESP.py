from machine import I2C, Pin
from uartfast import *
import ssd1306

class Oled:
    def init(self,width,height):
        i2c=I2C(scl=Pin(5),sda=Pin(4))
        self.oled=ssd1306.SSD1306_I2C(width, height, i2c)
    
    def text(self,txt,x,y):
        self.oled.text(txt,x,y)
    
    def show(self):
        self.oled.show()

    def fill(self,f):
        self.oled.fill(f)


u=UartRemote(0)
oled=Oled()
u.add_command('oledi',oled.init)
u.add_command('oledt',oled.text)
u.add_command("oleds",oled.show)
u.add_command("oledf",oled.fill)

u.loop()


"""
from uartfast import *
u=UartRemote(Port.S1)

u.send_receive("oledi","BB",64,48)
"""