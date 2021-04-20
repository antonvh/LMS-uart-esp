# Plot running graph using WebSockets

This example uses the Micropython Websocket server implementation found here (https://github.com/BetaRavener/upy-websocket-server).

It reads the `hub.motion.accelaration()` sensor of the Spike prime.

# Plot server on esp8266

On the ESP both the webserver and the uartremote server runs. We us HighCharts javascript implementation. The following commands are supported by `plot_svr.py':

- `ur.call('add_series','s','<series id>` adds a new series to the chart (by default the chart has one single series)
- `ur.call('series_name''is',<series number>,"<series name>")` sets the name of `series[series number]`
- `ur.call('title','s',"New title")` sets the title of the graph to `New title`
- `ur.call('yaxis','s','yaxis title')` sets the title of the y-axis
- `ur.call('data','f',[v0,v1,...vn])` send data to the chart, where the number v1 goes into series[0],until vn in series[n]. The number of series need to be created first.

The python script `plot_svr.py` sends the commands to the webclient (`plot_dyn.html`) using websockets. 

## Installation

### On the ESP8266

Copy the files `ws_connection.py`, `ws_server.py`, `plot.py` and `plot.html` to the esp8266.

On the ESP8266 you can choose to configure wifi to connect to Wifi.

Run `from plot import *` on the ESP8266. The webserver should start.

### On the SPIKE

Execute the progra, `plot_imu_SPIKE.py`.

## Connect using webbrowser.

Connect to the ESP8266 using a webbroser. Set the websocket address to the address that matches the one you see when starting the `plot.py` script.

