# Examples for LMS-uart-lib

These examples can be run without external sensors or hardware between an EV# and an ESP8266 board

## Simultaneous communication

Upload `sim_ESP.py` to the esp board, and `sim_EV4.py` to the EV3. Issue the following commands:

On the EV3
```
from sim_EV3 import *
```
On the ESP8266
```
from sim_ESP8266 import *
```
