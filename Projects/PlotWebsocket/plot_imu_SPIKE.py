import hub
from uartremote import *

def imu():
    return(list(hub.motion.accelerometer()))



u.add_command('imu',imu,'i')


