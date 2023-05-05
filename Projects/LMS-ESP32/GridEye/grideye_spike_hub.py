import hub
import math
from projects.uartremote import *

ur=UartRemote('D')

def sign(p):
    if p<0:
        return -1
    elif p>0:
        return 1
    else:
        return 0

def goto_zero():
    pos_e=motor_e.get()[1]
    power=-sign(pos_e)*20
    if power!=0:
    # -60 (omhoog) .. 45
      motor_e.run_for_degrees(abs(pos_e),power)
    pos_f=motor_f.get()[1]
    power=-sign(pos_f)*20
    if power!=0:
       # -70 (rechts) .. 145 (links)
        motor_f.run_for_degrees(abs(pos_f),power)

def move_delta(dx,dy):
    pos_e=motor_e.get()[1]+dy
    pos_f=motor_f.get()[1]+dx
    
    # -70 (rechts) .. 145 (links)
    if pos_e+dy>-45 and pos_e+dy<45:
        power=sign(pos_e)*20
        if power!=0:
       # -70 (rechts) .. 145 (links)
            motor_e.run_for_degrees(abs(pos_e),power)
    if pos_f+dx>-45 and pos_f+dx<90:
        power=sign(pos_f)*20
        if power!=0:
       # -70 (rechts) .. 145 (links)
            motor_f.run_for_degrees(abs(pos_f),power)
       
# Create your objects here.

motor_e = hub.port.E.motor
motor_e.mode([(1, 0), (2, 0), (3, 0), (0, 0)])
motor_f = hub.port.F.motor
motor_f.mode([(1, 0), (2, 0), (3, 0), (0, 0)])
goto_zero()
while True:
    #for i in range(1):
    try:
        ack,q=ur.call('get_pos')
        m,avg,mx,my=q
        dx=0
        dy=0
        if m>avg+3:
            ddx=mx-4
            ddy=my-4
            if ddx>0:
                dx=5
            elif ddx<0:
                dx=-5
            else:
                ddx=0
            if ddy>0:
                dy=2
            elif ddy<0:
                dy=-2
            else:
                ddy=0
            print(mx,my,dx,dy)
            move_delta(dx,dy)
    except:
       print('q=',q)
    # 300 .. 359 0..45
# Write your program here.

motor_e.run_to_position(-20)



