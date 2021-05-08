import hub
from utime import sleep_ms
from projects.uartremote import *


ur=UartRemote("A")

ws_opened=False


def init_chart():
    ur.call("add_series","s","ay")
    ur.call("add_series","s","az")
    ur.call("series_name",'Bs',0,'ax')
    ur.call("series_name",'Bs',1,'ay')
    ur.call("series_name",'Bs',2,'az')
    ur.call('title','s','Acceleration')
    ur.call('yaxis','s','acceleration (m/s^2)')
    


while True:
    acc=list(hub.motion.accelerometer())
    if ws_opened:
        ur.call('data','f',acc)
        sleep_ms(100)
    if ur.available():
        cmd,val=ur.receive_command(wait=False)
        if cmd=="wsopen":
            sleep_ms(1000) # wait until chart is initialized
            ws_opened=True
            init_chart()
    
