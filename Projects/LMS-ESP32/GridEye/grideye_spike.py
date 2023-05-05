from mindstorms import Motor
import math
from projects.uartremote import *

ur=UartRemote('D')

def goto_zero():
    pos_e=motor_e.get_position()
    if pos_e>200:
        pos_e=pos_e-360
    # -60 (omhoog) .. 45
    motor_e.run_for_degrees(-pos_e,20)
    pos_f=motor_f.get_position()
    if pos_f>200:
        pos_f-=360
    # -70 (rechts) .. 145 (links)
    motor_f.run_for_degrees(-pos_f,20)

def move_delta(dx,dy):
    pos_e=motor_e.get_position()
    pos_f=motor_f.get_position()
    if pos_e>200:
        pos_e=pos_e-360
    # -60 (omhoog) .. 45
    if pos_f>200:
        pos_f-=360
    # -70 (rechts) .. 145 (links)
    if pos_e<45 and pos_e+dy>-60:
        motor_e.start(-dy)
    elif pos_e<45 and dy<0:
        motor_e.start(-dy)
    elif pos_e>-60 and dy>0:
        motor_e.start(-dy)
           
    else:
        motor_e.start(0)
    if pos_f+dx<145 and pos_f+dx>-70:
        print("move dy",dx)
        motor_f.start(-dx)
    else:
        motor_f.start(0)

# Create your objects here.

motor_e = Motor('E')
motor_f = Motor('F')
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



