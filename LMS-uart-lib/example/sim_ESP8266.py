from uartremote import *
import time

u=UartRemote(0)

def led(v):
    print('led')
    for i in v:
        print(i)

u.add_command("led",led)


t_old=time.ticks_ms()+4000                      # wait 2 seconds before starting
q=u.flush()                                     # flush uart rx buffer
while True:
    if u.available():                           # check if a command is available
        u.wait_for_command()
    if time.ticks_ms()-t_old>1000:              # send a command every second
        t_old=time.ticks_ms()
        print("send imu")
        print("recv=",u.send_receive('imu'))    # send 'imu' command & receive result
