# Plot running graph using WebSockets

This example uses the Micropython Websocket server implementation found here (https://github.com/BetaRavener/upy-websocket-server).

It reads the `hub.motion.accelaration()` sensor of the Spike prime.

## Installation

### On the ESP8266

Copy the files `ws_connection.py`, `ws_server.py`, `plot.py` and `plot.html` to the esp8266.

On the ESP8266 you can choose to configure wifi to connect to Wifi.

Run `from plot import *` on the ESP8266. The webserver should start.

### On the SPIKE

Execute the progra, `plot_imu_SPIKE.py`.

## Connect using webbrowser.

Connect to the ESP8266 using a webbroser. Set the websocket address to the address that matches the one you see when starting the `plot.py` script.

