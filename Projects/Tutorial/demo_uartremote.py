from uartremote import *
import random

ur=UartRemote()

def led(nr,r,g,b):
    print('nr,r,g,b',nr,r,g,b)
    
def sensor():
    return random.randint(100,200)    

def mul(a,b):
    return a*b

ur.add_command(led)
ur.add_command(sensor,'repr')
ur.add_command(mul,'repr')

ur.loop()