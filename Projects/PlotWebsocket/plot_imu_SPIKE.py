
MAINPY="""
from plot import *
"""



import hub
from uartremote import *

def imu():
    return(list(hub.motion.accelerometer()))




u = UartRemote('A',debug=True)

u.add_command('imu',imu,'i')

# the code below for initating the ESP8266 using remote repl does not work.
# Therefore, start the `plot.py` script manually on th ESP8266

# print("Uart initialized")

# u.repl_activate()
# print(u.repl_run("print(123)"))
# print(u.repl_run(MAINPY),reply=False)
# print("loaded script")
# u.flush()
# print("Flushed")
# # sleep_ms(2000)

u.loop()
raise SystemExit