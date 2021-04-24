# GraphLog

This projects contains the code for drawing real-time charts in hwich data can be logged. 


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

Copy the files `ws_connection.py`, `ws_server.py`, `graphlog.py` and `graphlog.html` to the esp8266.

On the ESP8266 you can choose to configure wifi to connect to Wifi.

### On the SPIKE

Paste the program `SPIKE_graphlog.py` in a new project and run.

## Starting GraphLog.

When the prorgam starts on the SPIKE, the client and/or server address of the ESP8266 is shown. Open a browser to one of these networks, depending to which wifi network the system running the webbrowser is connected.
Set the websocket address to the the same address that matches the one to which your browser points. As soon as you start the websocket, a message is sent to the SPIKE which initializes the chart and starts logging the acceleration sensor.
