from projects.mpy_robot_tools.uartremote import *

ur=UartRemote("A")


import hub
import time

while True:
    ack,old_angle=ur.call('servo_get_angle',"repr",0)
    if hub.button.left.was_pressed():
        ack,joy=ur.call('servo_set_angle',"repr",0,old_angle-10)
    elif hub.button.right.was_pressed():
        ack,joy=ur.call('servo_set_angle',"repr",0,old_angle+10)
    time.sleep_ms(20)