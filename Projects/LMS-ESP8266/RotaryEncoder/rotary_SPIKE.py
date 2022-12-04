from spike import Motor
from projects.uartremote import *
from time import sleep_ms
import time

RESET="""
import machine
machine.soft_reset()
"""

MAINPY="""
from rotary import *
from uartremote import *
r=Rotary(4,5)

ur=UartRemote()

def rotary():
    return r.value()


ur.add_comand(rotary,'i')

ur.loop()
"""




ur=UartRemote("A") # connect ESP to port A

ur.flush() # remove everything from rx buffer

ur.repl_activate()
print(ur.repl_run("print('Repl Tested')")) # check remote repl
ur.repl_run(RESET,reply=False) # to re-load library, soft reset is needed
sleep_ms(200)
ur.repl_activate()
ur.repl_run(MAINPY,reply=False)

# Sleep is needed for the uart to stablize???
sleep_ms(1000)

print(ur.call('echo','repr',"Echo test is working"))

old_val=0
while True:
    cmd,val=ur.call('rotary')
    if old_val!=val:
        print("rotary=",val)
        old_val=val