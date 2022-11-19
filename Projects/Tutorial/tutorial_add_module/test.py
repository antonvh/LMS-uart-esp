import random

def sensor():
    return random.randint(100,200)    

def mul(a,b):
    return a*b

def add_commands(ur):               # add this function to evenry module
                                    # you want to load and
                                    # define the commands you would like to
                                    # expose over the UartRemote connection
    ur.add_command(sensor,'repr')
    ur.add_command(mul,'repr')

