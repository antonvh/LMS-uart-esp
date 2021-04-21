import hub
from utime import sleep_ms,ticks_ms,ticks_diff
from projects.uartremote import *


ur=UartRemote("A") # connect ESP to port A

ws_opened=False


def init_chart():
    ur.call("add_series","s","ay")
    ur.call("add_series","s","az")
    ur.call("series_name",'Bs',0,'ax')
    ur.call("series_name",'Bs',1,'ay')
    ur.call("series_name",'Bs',2,'az')
    ur.call('title','s','Acceleration')
    ur.call('yaxis','s','acceleration (m/s^2)')
    

refresh_ms=100  # refresh every 100ms
t_old=ticks_ms()

while True:
    acc=list(hub.motion.accelerometer())
    if ws_opened:
        t_ms=ticks_ms()
        if ticks_diff(t_ms,t_old)>refresh_ms:
            ur.call('data','f',acc)
            t_old=t_ms
    if ur.available():
        cmd,val=ur.receive_command(wait=False)
        if cmd=="wsopen": # if websocket is opened, initialize chart
            sleep_ms(500) # wait until chart is initialized
            ws_opened=True
            init_chart()
    
