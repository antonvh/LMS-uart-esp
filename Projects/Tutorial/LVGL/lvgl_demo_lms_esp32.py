from uartremote import *
import espidf as esp
import lvgl as lv
from ili9XXX import ili9341,LANDSCAPE
from xpt2046 import xpt2046

#init display
disp = ili9341(miso=12, mosi=13, clk=14, cs=15, dc=23, rst=25,
               backlight=-1,power=-1,
               width=320, height=240, rot=LANDSCAPE)
# use same SPI as display, init touch
touch = xpt2046(spihost=esp.HSPI_HOST,cs=26,transpose=False,
                cal_x0=3865, cal_y0=329, cal_x1=399, cal_y1=3870)


arc = lv.arc(lv.scr_act())
arc.set_range(0,360)
arc.set_bg_angles(0,360)
arc.set_size(150,150)
arc.align(lv.ALIGN.CENTER,0,0)
arc.set_value(100)

slider = lv.slider(lv.scr_act())
slider.set_width(200)
slider.align(lv.ALIGN.CENTER,0,-100)
slider.set_range(0,360)

label1 = lv.label(lv.scr_act())
label1.set_long_mode(lv.label.LONG.SCROLL_CIRCULAR)         # Circular scroll
label1.set_width(150)
label1.set_text("Demo using LVGL library. ")
label1.align(lv.ALIGN.CENTER, 0, 100)
ur=UartRemote()

def show_angle(angle):
    arc.set_value(angle%360)
    slider.set_value(angle%360,1)
    
ur.add_command(show_angle)

ur.loop()