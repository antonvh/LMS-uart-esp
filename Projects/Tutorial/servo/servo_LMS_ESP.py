from uartremote import *
from servo import *

servos=[]
for pin in [21,22,23,25]:
    servos.append(Servo(pin,angle=360,min_us=500,max_us=2500))

angles=[0,0,0,0]

def servo_set_angle(nr,angle):
    global angles
    s=servos[nr]
    s.write_angle(angle)
    angles[nr]=angle       # store angle
    
def servo_get_angle(nr):
    return angles[nr]


ur=UartRemote()
ur.add_command(servo_set_angle)
ur.add_command(servo_get_angle,'repr')


ur.loop()
    