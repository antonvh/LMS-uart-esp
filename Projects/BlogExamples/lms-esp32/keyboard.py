# module env

from machine import I2C,Pin
# init i2c bus
i2c=I2C(1,sda=Pin(5),scl=Pin(4))

KEYB_ADDR=95

def read_key():
    return i2c.readfrom(KEYB_ADDR,1) # read one byte containing key

def add_commands(ur):
    ur.add_command(read_key,'s')
    