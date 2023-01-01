from projects.mpy_robot_tools.uartremote import *
import hub

ur=UartRemote('A')
motor = hub.port.B.motor


motor.mode([(2,0)]) # absolute position, raw units

motor.preset(0)
while (True):
    m=motor.get()[0]
    ack,val=ur.call('show_angle','repr',m)
    