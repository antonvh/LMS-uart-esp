from projects.uartremote import *
import hub
from time import sleep_ms
ur=UartRemote('B')


c=hub.port.C
d=hub.port.D

c.motor.mode(3)

steer=0
speed=0

# remotely import module `keuboard`
ur.add_module('keyboard')

# print commands available after remotely importing module `test`
while True:
    try:
        ack,key=ur.call('read_key')
        if key==b'\xb4':   #left
            hub.display.show(hub.Image.ARROW_W)
            steer+=40
            if steer>160:
                steer=160
            c.motor.run_to_position(steer)
        elif key==b'\xb7': # right
            hub.display.show(hub.Image.ARROW_E)
            steer-=40
            if steer<-160:
                steer=-160
            c.motor.run_to_position(steer)
        elif key==b'\xb5': # up
            hub.display.show(hub.Image.ARROW_N)
            speed+=20
            if speed>100:
                speed=100
            d.motor.run_at_speed(speed)
        elif key==b'\xb6': # down
            hub.display.show(hub.Image.ARROW_S)
            speed-=20
            if speed<-100:
                speed=-100
            d.motor.run_at_speed(speed)
        elif key != b'\x00':
            hub.display.show(key.decode('utf-8'))
        sleep_ms(20)
    except KeyboardInterrupt:
        print('interrupted!')
        break
    except:
        print("Error",ack,key)

