# module test.py

def led(n,r,g,b):
  # code for turning on led n using color (r,g,b)
  # now we only print the received data
  print(n,r,g,b)

def read_temp():
  # code for reading a temperature sensor
  import random
  return random.randint(15,40)

def collect_data():
  # code for pulling tuple
  return [('ABC',123),('ABC',123.456)]

def add_commands(ur): # call for adding the functions in this module to UartRemote commands
  ur.add_command(led) # does not return any value
  ur.add_command(read_temp,'i') # returns an integer
  ur.add_command(collect_data,'repr') # returns string



