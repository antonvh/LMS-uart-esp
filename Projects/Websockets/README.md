# Websockets

A small WebSocket implementation can be found on https://github.com/BetaRavener/upy-websocket-server.

To run this demo, connect the ESP8266 to the wifi network. Once a succesfull connection is established, the ssid and the webkey are stored in flash and every reboot, the connection is reastablished.

_Note_: this demo is not stable yet, but shows the potential of running a web server with websockets on the ESP8266.

# ESP8266

Run 

```
import websocket_demo
```

```
>>> import websocket_demo                                                                                                                             
WebSocket started on ws://192.168.x.y:80                                                                                                            
Started WebSocket server.                   
```

Browse to the the IP address that is shown. The websocket is ready and can be tested by sending a string in the browser.

The files in the ESP8266 direcotry need to be uploaded to the ESP8266.

In the function `+check_socket_state` the socket is returns state 3 and closes. To prevent this, in the file `ws_connection.py` the following lines were commented out:

```python
 def _check_socket_state(self):
        self._need_check = False
        sock_str = str(self.socket)
        state_str = sock_str.split(" ")[1]
        state = int(state_str.split("=")[1])
        print("check_socket_state",state_str,state)
        #if state == 3:
        #    self.client_close = True
```

# EV3

For testing the websocket, run

```
import test_websocket
```

Now, the EV3 sends a command with a string as data over the uart to the ESP8266. The string is whown in de webbrowser. The test sends 1000 strings, and determines the transfer rate.
When the connection is stuck, the browser can be reloaded.
