"""
Calibrate magneto meter HMC5883L
"""


from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient
import time
import random
#from uartremote import *

from hmc5883l import HMC5883L

sensor = HMC5883L(scl=5, sda=4)


class TestClient(WebSocketClient):
    
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            value=sensor.read() # read magnetic field components
            s=",".join(["%f"%i for i in value])
            self.connection.write(s) # send to websocket client
            
            if not msg:
                return
            msg = msg.decode("utf-8")
            items = msg.split(" ")
            cmd = items[0]
            if cmd == "Open":
                #self.connection.write(cmd + " World")
                print("ws connection opened")
                #u.disable_repl_locally()
                #u.flush()
                #u.send_command("wsopen",'s','ok')
        except ClientClosedError:
            self.connection.close()


class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__("graphlog.html", 2)

    def _make_client(self, conn):
        return TestClient(conn)

PERIOD=100
# u=UartRemote()
# u.disable_repl_locally()
server = TestServer()
server.start()
t_old=time.ticks_ms()
try:
    while True:
        t=time.ticks_ms()
        if time.ticks_diff(t,t_old)>PERIOD:
            t_old=t
            server.process_all()

except KeyboardInterrupt:
    pass
server.stop()
