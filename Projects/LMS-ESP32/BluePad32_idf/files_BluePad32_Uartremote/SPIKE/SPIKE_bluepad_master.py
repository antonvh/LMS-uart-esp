from projects.uartremote import *
from utime import sleep_ms,ticks_ms,ticks_diff
import time
import hub
u=UartRemote("B")

def norm(x):
    return int((x+512)/204.8-0.5)

def connected(dummy):
    print("gamepad is connected")
    
def disconnected(dummy):
    print("gamepad is connected")

led=0
old_buttons=0
old_dpad=0

    #print(buttons,dpad,lx,ly,rx,ry)
    

t_old=ticks_ms()+2000     
while True:
    #if u.available():
    #        u.reply_command(u.receive_command())
    if hub.button.left.was_pressed():
        led+=1
        led&=15;
        u.call('led','B',led)
        
    if hub.button.right.was_pressed():
        print("pressed")
        rumble_force=0xc0
        rumble_duration=0xc0
        u.call('rumble','2B',rumble_force,rumble_duration)

    if time.ticks_ms()-t_old>1000:              # send a command every second
        t_old=time.ticks_ms()
        print("send servo")
        print("recv=",u.call('servo','Bi',123,500))
        
    ack,resp=u.call('gamepad')
    try:
        buttons,dpad,lx,ly,rx,ry=resp
        if buttons!=old_buttons:
            old_buttons=buttons
            print(buttons)
        if dpad!=old_dpad:
            old_dpad=dpad
            print(dpad)
        x=norm(lx)
        y=norm(ly)
        hub.display.show(" ")
        hub.display.pixel(x,y,9)
        x=norm(rx)
        y=norm(ry)
        #hub.display.show(" ")
        hub.display.pixel(x,y,8)
    except:
        print("error",resp)
    sleep_ms(10)


