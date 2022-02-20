# demonstration program to be used together with BluePad32_uartremote running on ESP32

from projects.uartremote import *
from utime import sleep_ms,ticks_ms,ticks_diff
import hub
u=UartRemote("B") # change port here

def norm(x):
    return int((x+512)/204.8-0.5)

def connected(dummy):
    print("gamepad is connected")
    
def disconnected(dummy):
    print("gamepad is connected")

led=0
rumble_force=0
rumble_duration=0
old_buttons=0
old_dpad=0
t=ticks_ms()
def gamepad(buttons,dpad,lx,ly,rx,ry):
    global led
    global old_buttons
    global old_dpad
    
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
    hub.display.pixel(x,y,5)
    if hub.button.left.was_pressed():
        led+=1
        led&=15;
        
    if hub.button.right.was_pressed():
        print("pressed")
        rumble_force=0xc0
        rumble_duration=0xc0
        rumble=True
    else:
        rumble_force=0
        rumble_duration=0
    return (led,rumble_force,rumble_duration)
    #print(buttons,dpad,lx,ly,rx,ry)
    

u.add_command(connected)
u.add_command(disconnected)
u.add_command(gamepad,"3B")

    
u.loop()



