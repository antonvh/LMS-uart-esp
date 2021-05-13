import hub
from utime import sleep_ms,ticks_ms,ticks_diff
from projects.uartremote import *

WIFI="""import network
for i in (network.AP_IF, network.STA_IF):
    iface = network.WLAN(i)
    if iface.active():
        print("WebSocket started on ws://%s" % iface.ifconfig()[0])



#done
"""

GRAPHLOG="""from graphlog import *
"""

ur=UartRemote("D") # connect ESP to port A


ur.repl_activate()
print(ur.repl_run("print('Repl Tested')"))
print(ur.repl_run(WIFI))
print(ur.repl_run(GRAPHLOG,reply=False))
print("script is running")
ur.flush()
ws_opened=False


def init_chart():
    ur.call("add_series","repr","ay")
    ur.call("add_series","repr","az")
    ur.call("series_name",'repr',0,'ax')
    ur.call("series_name",'repr',1,'ay')
    ur.call("series_name",'repr',2,'az')
    ur.call('title','repr','Acceleration')
    ur.call('yaxis','repr','acceleration (m/s^2)')


refresh_ms=100# refresh every 100ms
t_old=ticks_ms()

while True:
    acc=list(hub.motion.accelerometer())
    if ws_opened:
        t_ms=ticks_ms()
        if ticks_diff(t_ms,t_old)>refresh_ms:
            ur.call('data','repr',acc)
            t_old=t_ms
    if ur.available():
        cmd,val=ur.receive_command()
        print("received:",cmd,val)
        if cmd=="wsopen": # if websocket is opened, initialize chart
            print("WebSocket opened")
            sleep_ms(500) # wait until chart is initialized
            ws_opened=True
            init_chart()



ur.flush()
print("Flushed")

