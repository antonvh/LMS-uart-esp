from mindstorms import MSHub
from projects.uartremote import *
from hub import port

# Create your objects here.
ms_hub = MSHub()
ur = UartRemote('E')

# Write your program here.
ms_hub.speaker.beep()

# Test remote connection
print(ur.call('echo','repr','Uart command loop tested with echo'))

while True:
    # print(ur.call('echo','repr','Uart command loop tested with echo'))
    ack, payload = ur.call('blob')
    if ack == 'bloback':
        if len(payload) == 2:
            direction = int((payload[0]-60)/2) # x coordinate of blob
            distance = int(payload[1]/3)+20
            port.A.motor.pwm(distance+direction)
            port.B.motor.pwm(-distance+direction)
        else:
            port.A.motor.pwm(0)
            port.B.motor.pwm(0)
    else:
        print(ack, payload)
        port.A.motor.pwm(0)
        port.B.motor.pwm(0)