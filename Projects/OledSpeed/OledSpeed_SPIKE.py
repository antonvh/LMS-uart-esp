from spike import Motor
import time
from projects.uartremote import *

MAINPY="""
from oled_speed import *
"""

ur=UartRemote("E") # connect ESP to port A


ur.flush() # remove evernything
ur.repl_activate()
print(ur.repl_run("print('Repl Tested')"))
# reset esp8266; otherwise oled_speed library is not import correctly after first time
ur.repl_run("import machine")
ur.repl_run("machine.reset()")
time.sleep_ms(500)
ur.flush() # remove evernything
ur.repl_activate()
ur.repl_run(MAINPY,reply=False)
print("loaded script")






print("OledSpeed test started")
print("turn motor")
motor=Motor("C")
old_speed=0
while True:
    speed=motor.get_degrees_counted()
    if old_speed!=speed:
        old_speed=speed
        print(speed)
        print(ur.call('speed','B',speed))
