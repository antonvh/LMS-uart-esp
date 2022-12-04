"""
Example code for driving a ssd1306 i2c OLED screen. 
"""



from machine import I2C, Pin
import ssd1306

from uartremote import *

class Oled:
    def __init__(self,width=128,height=64):
        i2c=I2C(scl=Pin(4),sda=Pin(5))
        self.oled=ssd1306.SSD1306_I2C(width, height, i2c)
        for i in range(40):
            self.oled.fill(0)
            self.oled.text("Readyl!",10,i+5)
            self.oled.show()
        
    
    def text(self,txt,x,y):
        self.oled.text(txt,x,y)
    
    def show(self):
        self.oled.show()

    def fill(self,f):
        self.oled.fill(f)
    
    def line(self,x1,y1,x2,y2,color):
        self.oled.line(x1,y1,x2,y2,color)

    def pixel(self,x1,y1,color):
        self.oled.pixel(x1,y1,color)

# initialize UartRemote library
u=UartRemote()
# initialize Oled instance
oled=Oled()
# define different commands
u.add_command(oled.__init__,name='oledi')
u.add_command(oled.text,name='oledt')
u.add_command(oled.show,name="oleds")
u.add_command(oled.fill,name="oledf")
u.add_command(oled.line,name="oledl")
u.add_command(oled.pixel,name="oledp")

# wait for a command in an endless loop
u.loop()

