
"""
Master:

from uartremote import *
u=UartRemote(esp32_rx=12, esp32_tx=13)

u.call('add_series','s',"een")
u.call('add_series','s','twee')
u.call('title','s','Dit is de nieuwe titel')
u.call('yaxis','s','Motor Posision (degrees)')

u.call('data','f',[3,1,2])
u.call('data','f',[3,1,2])
u.call('data','f',[1,2,3])
u.call('data','f',[1,2,3])
u.call('series_name','is',0,"Motor A")
u.call('series_name','is',1,"Motor B target")
u.call('series_name','is',2,"Motor C")


"""



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
            if u.available():
                (cmd,value)=u.receive_command()
                u.send_command(cmd+"ack",'s','ok')
                print(value)
                if cmd=="data":
                    #try:
                    s="data "+",".join(["%f"%i for i in value])
                    self.connection.write(s)
                    #except:
                    #    pass
                elif cmd=="title":
                    self.connection.write("title %s"%value)
                elif cmd=="yaxis":
                    self.connection.write("yaxis %s"%value)
                elif cmd=="add_series":
                    self.connection.write("add_series %s"%value)
                elif cmd=="series_name":
                    self.connection.write("series_name %d,%s"%(value[0],value[1]))
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
        super().__init__("plot_dyn.html", 2)

    def _make_client(self, conn):
        return TestClient(conn)

u=UartRemote()
#u.disable_repl_locally()
#u.flush()
server = TestServer()
server.start()
try:
    while True:
        server.process_all()
except KeyboardInterrupt:
    pass
server.stop()
