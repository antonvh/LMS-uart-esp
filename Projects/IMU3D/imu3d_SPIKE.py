import hub
from utime import sleep_ms,ticks_ms,ticks_diff,sleep
from projects.uartremote import *

MAINPY="""from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient
import time

from uartremote import *

class TestClient(WebSocketClient):

    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()

            if u.available():
                (cmd,value)=u.receive_command()
                u.send_command(cmd+"ack",'repr','ok')
                print(value)
                s=cmd+" "+",".join(["%f"%i for i in value])
                self.connection.write(s)
            
            if not msg:
                return
            msg = msg.decode("utf-8")
            items = msg.split(" ")
            cmd = items[0]
            if cmd == "wsopen":
                #self.connection.write(cmd + " World")
                print("ws connection opened")
                #u.disable_repl_locally()
                #u.flush()
                u.send_command("wsopen",'repr','ok')
            elif cmd=="euler":
                u.send_command("euler",'repr','ok')
        except ClientClosedError:
            self.connection.close()


class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__("graphlog.html", 2)

    def _make_client(self, conn):
        return TestClient(conn)

u=UartRemote()
u.disable_repl_locally()
server = TestServer()
server.start()
try:
    while True:
        server.process_all()
except KeyboardInterrupt:
    pass
server.stop()
"""

WIFI="""import network
for i in (network.AP_IF, network.STA_IF):
    iface = network.WLAN(i)
    if iface.active():
        print("WebSocket started on ws://%s" % iface.ifconfig()[0])
"""


ur=UartRemote("E") # connect ESP to port A


ur.repl_activate()
print(ur.repl_run("print('Repl Tested')"))
print(ur.repl_run(WIFI))
print(ur.repl_run(MAINPY,reply=False))
print("script is running")
ur.flush()
ws_opened=False
sleep_ms(1000)

refresh_ms=100# refresh every 100ms
t_old=ticks_ms()

ACC='acc'
GYRO='gyro'
EULER='euler'

cur_mode=EULER

while True:
    if cur_mode==ACC:
        value=list(hub.motion.accelerometer())
    elif cur_mode==EULER:
        value=list(hub.motion.yaw_pitch_roll())
    if ws_opened:
        t_ms=ticks_ms()
        if ticks_diff(t_ms,t_old)>refresh_ms:
            ur.call(cur_mode,'repr',value)
            t_old=t_ms
    if ur.available():
        cmd,val=ur.receive_command()
        print("received:",cmd,val)
        if cmd=="wsopen": # if websocket is opened, initialize chart
            print("WebSocket opened")
            sleep_ms(500) # wait until chart is initialized
            ws_opened=True
        elif cmd=="acc":
            cur_mode=ACC
        elif cmd=="euler":
            print("cmd=",cmd)
            cur_mode="euler"


ur.flush()
print("Flushed")

