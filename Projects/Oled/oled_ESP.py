"""
Example code for driving a ssd1306 i2c OLED screen. 
"""



from machine import I2C, Pin
from uartremote import *
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
    
    def line(self,x1,y1,x2,y2,color):
        self.oled.line(x1,y1,x2,y2,color)

    def pixel(self,x1,y1,color):
        self.oled.line(x1,y1,color)

# initialize UartRemote library
u=UartRemote(0)
# initialize Oled instance
oled=Oled()
# define different commands
u.add_command('oledi',oled.init)
u.add_command('oledt',oled.text)
u.add_command("oleds",oled.show)
u.add_command("oledf",oled.fill)
u.add_command("oledl",oled.line)
u.add_command("oledp",oled.pixel)

# wait for a command in an endless loop
u.loop()


