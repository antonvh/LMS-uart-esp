import time
from uartfast import *
    
def imu():
    return('f',[12.3,11.1,180.0])

u=UartRemote(Port.S1)
u.add_command("imu",imu)

t_old=time.ticks_ms()+4000                      # wait 2 seconds before starting
q=u.flush()                                     # flush uart rx buffer
while True:
    if u.available():                           # check if a command is available
        u.wait_for_command()
    if time.ticks_ms()-t_old>1000:              # send a command every second
        t_old=time.ticks_ms()
        print("send led")                       # send 'led' command with data
        print("recv=",u.send_receive('led','b',[1,2,3,4]))
