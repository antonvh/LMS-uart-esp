from ws_connection import ClientClosedError
from ws_server import WebSocketServer, WebSocketClient
from machine import UART
from uartremote import *




u=UartRemote()


class TestClient(WebSocketClient):
    def __init__(self, conn):
        super().__init__(conn)

    def process(self):
        try:
            msgReceived = ''
            if u.uart.any():
                cmd,data=u.receive()
                self.connection.write(data)
                u.send('ack','s','ok')


            msg = self.connection.read()
            if not msg:
                return
            msg = msg.decode("utf-8")
            self.connection.write(msg)
            print (msg)

        except ClientClosedError:
            self.connection.close()


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
