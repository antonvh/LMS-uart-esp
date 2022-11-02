from projects.uartremote import *
import hub
from time import sleep_ms,ticks_ms,ticks_diff
ur=UartRemote('B')

ur.add_module('etchasketch')

ur.call('clear')

MotorF=hub.port.F.motor
MotorA=hub.port.A.motor

MotorF.mode([(2,0)]) # absoulute position, raw units
MotorA.mode([(2,0)])

MotorA.preset(0)
MotorF.preset(0)
x=0
y=0
old_x=0
old_y=0

colors=[(30,0,0),(0,30,0),(0,0,30),(0,0,0)]

hub.button.left.was_pressed()
hub.button.right.was_pressed()
cur_col=0
n=0
cursor=1
while True:
        n+=1
        if hub.button.left.was_pressed():
            cur_col-=1
            cur_col%=4
            print("left",cur_col)
        if hub.button.right.was_pressed():
            cur_col+=1
            cur_col%=4
            #print("right",cur_col)
        colr=colors[cur_col][0]
        colg=colors[cur_col][1]
        colb=colors[cur_col][2]
        ma=MotorA.get()[0]
        mf=MotorF.get()[0]
        x=ma//20
        y=mf//20
        if x<0:
            x=7 # wrap around
            MotorA.preset(7*20)
        if y<0:
            y=7
            MotorF.preset(7*20)
        if x>7:
            x=0
            MotorA.preset(0)
        if y>7:
            y=0
            MotorF.preset(00)
        if x!=old_x or y!=old_y:
            ack,val=ur.call('plotxy','5B',old_x,old_y,colr,colg,colb)
            print(x,y)
            old_x=x
            old_y=y
            ack,val=ur.call('plotxy','5B',x,y,cursor*colr,cursor*colg,cursor*colb)
        if n==100:
            cursor=1-cursor
            n=0
            ack,val=ur.call('plotxy','5B',x,y,cursor*colr,cursor*colg,cursor*colb)

    #except KeyboardInterrupt:
    #   print('interrupted!')
    #    break
    #except:
    #    print("Error",ack,key)

