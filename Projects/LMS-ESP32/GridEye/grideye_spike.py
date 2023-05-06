from mindstorms import Motor
import math
from mindstorms.control import wait_for_seconds
# wait for 3 seconds (pause the program flow)
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

def move_delta(dxr,dyr):
    dx=int(dxr)
    dy=int(dyr)
    pos_e=motor_e.get_position()
    pos_f=motor_f.get_position()
    if pos_e>180:
        pos_e-=360
    if pos_f>180:
        pos_f-=360
    print(pos_e,pos_f,dy,dx)
    """ positive is downwards. dy+ need to move up
    """
    if dy<0:
        if pos_e<45:
            #motor_e.run_for_degrees(dy,-50)
            motor_e.start(-dy)
    elif dy>0:
        if pos_e>-60:
            #motor_e.run_for_degrees(dy,50)
            motor_e.start(-dy)
    else:
        motor_e.start(0)
    ''' motor f: clockwise = pos. Dx=positive -> clockwise
    '''
    if dx<0:
        if pos_f<145 :
            print("f<145,dx",-dx)
            #motor_f.run_for_degrees(dx,50)
            motor_f.start(-dx)
    elif dx>0:
        if pos_f>-70:
            print("f>-70,dx",dx)
            #motor_f.run_for_degrees(dx,-50)
            motor_f.start(-dx)
    else:
        motor_f.start(0)
    
# Create your objects here.

motor_e = Motor('E')
motor_f = Motor('F')
goto_zero()
while True:
    wait_for_seconds(0.05)
    for i in range(1):
    #try:
        ack,q=ur.call('get_pos')
        m,avg,mx,my=q
        dx=0
        dy=0
        if m>avg+3:
            ddx=mx-3.5
            ddy=my-3.5
            move_delta(ddx,ddy)
    #except:
    #   print('q=',q)
    # 300 .. 359 0..45
# Write your program here.

motor_e.run_to_position(-20)



