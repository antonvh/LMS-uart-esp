from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient
import time
import random
from uartremote import *

class TestClient(WebSocketClient):
    t=30
    h=50
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            (cmd,value)=u.call('imu')
            print(value)
            #vals=[int(i) for i in value]
            try:
                self.connection.write("%d,%d,%d"%(value[0],value[1],value[2]))
            except:
                # should be u.flush(), but that does not seem to work????
                u.uart.read()
            time.sleep(0.2)
            if not msg:
                return
            msg = msg.decode("utf-8")
            items = msg.split(" ")
            cmd = items[0]
            if cmd == "Hello":
                self.connection.write(cmd + " World")
                print("Hello World")
        except ClientClosedError:
            self.connection.close()


class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__("plot.html", 2)

    def _make_client(self, conn):
        return TestClient(conn)

u=UartRemote()
u.disable_repl_locally()
u.flush()
server = TestServer()
server.start()
try:
    while True:
        server.process_all()
except KeyboardInterrupt:
    pass
server.stop()
