import hub
from utime import sleep_ms,ticks_ms,ticks_diff
from projects.uartremote import *

WIFI="""import network
for i in (network.AP_IF, network.STA_IF):
    iface = network.WLAN(i)
    if iface.active():
        print("WebSocket started on ws://%s" % iface.ifconfig()[0])
"""

GRAPHLOG="""from graphlog import *
"""

ur=UartRemote("A") # connect ESP to port A


ur.flush() # remove evernything
# try to enable repl if esp is still in non_repl mode
ur.send_command("enable repl",'s','ok')
print("response enable repl",ur.uart.read(100))


ur.repl_activate()
print(ur.repl_run("print('Repl Tested')"))
print(ur.repl_run(WIFI))
print(ur.repl_run(GRAPHLOG,reply=False))
print("script is running")
ur.flush()
ws_opened=False


def init_chart():
    ur.call("add_series","s","ay")
    ur.call("add_series","s","az")
    ur.call("series_name",'Bs',0,'ax')
    ur.call("series_name",'Bs',1,'ay')
    ur.call("series_name",'Bs',2,'az')
    ur.call('title','s','Acceleration')
    ur.call('yaxis','s','acceleration (m/s^2)')


refresh_ms=100# refresh every 100ms
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
        print("received:",cmd,val)
        if cmd=="wsopen": # if websocket is opened, initialize chart
            print("WebSocket opened")
            sleep_ms(500) # wait until chart is initialized
            ws_opened=True
            init_chart()



ur.flush()
print("Flushed")

