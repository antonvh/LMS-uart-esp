from uartremote import *
u=UartFast(Port.S1)

while True:
    print(u.send_receive('acc'))