# Demo for joystick with servo
# connected a M5stack i2c joystick to the Grove port and a servo to pin21

from projects.uartremote import *
from utime import sleep_ms,ticks_ms,ticks_diff
import struct
import time
import hub
u=UartRemote("B")


joy_addr=0x52

while True:
    ack,joy=u.call('i2c_read','2B',0x52,3)
    joy_x,joy_y,joy_b=struct.unpack('3B',joy)
    ser_pos=int(joy_x/256*180)
    ack,jnk=u.call('servo','>Bi',1,ser_pos)
    sleep_ms(50)
