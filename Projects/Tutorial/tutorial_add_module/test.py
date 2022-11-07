import random

def sensor():
    return random.randint(100,200)    

def mul(a,b):
    return a*b

def add_commands(ur):
    ur.add_command(sensor,'repr')
    ur.add_command(mul,'repr')

