from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient
import time
import random

class TestClient(WebSocketClient):
    t=30
    h=50
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            self.t+=random.randint(0,10)-5
            self.h+=random.randint(0,20)-10
            self.connection.write("%d,%d"%(self.t,self.h))
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


server = TestServer()
server.start()
try:
    while True:
        server.process_all()
except KeyboardInterrupt:
    pass
server.stop()
