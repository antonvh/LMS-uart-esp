from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient
import time

class TestClient(WebSocketClient):
    count=0
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msg = self.connection.read()
            self.connection.write("World %d"%self.count)
            print("count=",self.count)
            self.count+=1
            # if not msg:
            #     return
            # msg = msg.decode("utf-8")
            # items = msg.split(" ")
            # cmd = items[0]
            # if cmd == "Hello":
            #     self.connection.write(cmd + " World")
            #     print("Hello World")
        except ClientClosedError:
            print("ClientClosedError exception")
            #self.connection.close()


class TestServer(WebSocketServer):
    def __init__(self):
        super().__init__("test.html", 2)

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
