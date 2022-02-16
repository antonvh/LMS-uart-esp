# main.py demo uartremote loop, when running this will 
#   prevent use of USB rshell, use webshell
from uartremote import *
ur=UartRemote()         # initialize uartremote on default uart and default uart pins
ur.loop()               # start listing for commands received from the remote instance