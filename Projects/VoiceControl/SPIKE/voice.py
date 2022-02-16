from projects.uartremote import *
from utime import sleep_ms,ticks_ms,ticks_diff
import hub
u=UartRemote("B")

c=hub.port.C
d=hub.port.D

c.motor.mode(3)
c.motor.run_to_position(0)

steer=0
speed=0
def command(cmd):
    global speed
    global steer
    print("Command: ",cmd)
    if cmd==0:
        hub.display.show(hub.Image.ARROW_N)
        speed+=20
        if speed>100:
            speed=100
        d.motor.run_at_speed(speed)
    elif cmd==1:
        hub.display.show(hub.Image.ARROW_S)
        speed-=20
        if speed<-100:
            speed=-100
        d.motor.run_at_speed(speed)

    elif cmd==2:
        hub.display.show(hub.Image.ARROW_W)
        steer+=40
        if steer>160:
            steer=160
        c.motor.run_to_position(steer)
    elif cmd==3:
        hub.display.show(hub.Image.ARROW_E)
        steer-=40
        if steer<-160:
            steer=-160
        c.motor.run_to_position(steer)
    elif cmd==4:
        hub.display.show(hub.Image.NO)
        speed=0
        d.motor.run_at_speed(speed)

    print("speed=",speed,"steer=",steer)

u.add_command(command)


u.loop()



