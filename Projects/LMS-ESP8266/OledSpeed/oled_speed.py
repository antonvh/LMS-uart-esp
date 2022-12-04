from machine import I2C, Pin
import ssd1306
import framebuf
import random

from uartremote import *

i2c = I2C(scl=Pin(5), sda=Pin(4))  # open i2c on Pin 4 and 5
oled= ssd1306.SSD1306_I2C(128, 64, i2c, 0x3c) # initialize oled ssd1306 display

f=open('images.bin','rb') # open binary file containing 17 images of 1024 bytes each for speeds as in array speeds

# images for the following speeds:
speeds=[3,9,13,18,24,29,35,41,47,53,60,66,72,78,84,89,93,97]

def speed(s):
    if s>100: s=100
    if s<0: s=0
    for i,sp in enumerate(speeds):
        if s<=sp:
            break
    f.seek(i*1024) # skip to the ith image
    d=bytearray(f.read(1024)) # read image
    fbuf=framebuf.FrameBuffer(d, 128, 64, framebuf.MONO_HLSB) # fill framebuffer with image
    oled.blit(fbuf,0,0) # blit framebuffer to posision 0,0
    oled.show()  # show current screen

u=UartRemote()
u.add_command(speed) # add command 'speed'
u.loop() 