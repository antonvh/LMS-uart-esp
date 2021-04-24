# GraphLog

This projects contains the code for drawing real-time charts in hwich data can be logged. 


# Plot server on esp8266

On the ESP both the webserver and the uartremote server runs. We us HighCharts javascript implementation. The following commands are supported by `plot_svr.py':

- `ur.call('add_series','s','<series id>` adds a new series to the chart (by default the chart has one single series)
- `ur.call('series_name''is',<series number>,"<series name>")` sets the name of `series[series number]`
- `ur.call('title','s',"New title")` sets the title of the graph to `New title`
- `ur.call('yaxis','s','yaxis title')` sets the title of the y-axis
- `ur.call('data','f',[v0,v1,...vn])` send data to the chart, where the number v1 goes into series[0],until vn in series[n]. The number of series need to be created first.

The python script `graphlog.py` sends the commands to the webclient (`graphlog.html`) using websockets. 

## Installation

### On the ESP8266
Copy the files `ws_connection.py`, `ws_server.py`, `graphlog.py` to the esp8266.
#### When your LMS-wifi board is connected to your wifi
Copy the file `graphlog.html` to the esp8266.
See the wiki about [connecting to Wifi](https://github.com/antonvh/LMS-uart-esp/wiki/Configure-webrepl).
#### When your LMS-wifi board in Access Point/Hotspot mode
Open the project file `graphlog_local.html` in a browser.

### On the SPIKE
Paste `Libraries/UartRemote/MicroPython/SPIKE/install_uartremote.py` in a new project and run once.
Paste the program `SPIKE_graphlog.py` in a new project.

## Running GraphLog.
1. Start the program on the SPIKE hub
2. The client and/or server address of the ESP8266 is shown in the print console
3. If your LMS-wifi board is connected to your WLAN: Open a browser to the web address shown & and connect to ws on the same address. Done!
4. If your LMS-wifi board is in AP mode, switch your Wifi network to the LMS-wifi board network (`MicroPython-xxxxxx`)
5. Open the project file `graphlog_local.html` in a browser.
6. Click connect.

Set the websocket address to the the same address that matches the one to which your browser points. As soon as you start the websocket, a message is sent to the SPIKE which initializes the chart and starts logging the acceleration sensor.

