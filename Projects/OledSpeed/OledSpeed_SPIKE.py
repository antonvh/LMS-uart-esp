from spike import Motor
from projects.uartremote import *

MAINPY="""
from oled_speed import *
"""

ur=UartRemote("A") # connect ESP to port A


ur.flush() # remove evernything
# try to enable repl if esp is still in non_repl mode
ur.send_command("enable repl",'s','ok')
print("response enable repl",ur.uart.read(100))

ur.repl_activate()
print(ur.repl_run("print('Repl Tested')"))
print(ur.repl_run(MAINPY,reply=False))
print(ur.uart.read(1024))
print("loaded script")



print("OledSpeed test started")
print("turn motor")
motor=Motor("E")
old_speed=0
while True:
    speed=motor.get_degrees_counted()
    if old_speed!=speed:
        old_speed=speed
        print(speed)
        print(ur.call('speed','b',speed))
