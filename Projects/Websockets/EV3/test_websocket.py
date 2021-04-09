import time
from uartremote import *

u=UartRemote(Port.S1)
time.sleep(5) # wait 5 seconds before starting
u.flush()

#t_start=time.time()
for i in range(1000):
    if u.available():
        cmd,value=u.receive()
        u.send('ack','s','ok')
    q=u.send_receive('cmd','s','hierpdepiep %i'%i)
    time.sleep(0.1)

#t_delta=time.time()-t_start
#print("1000 transactions in %fs. Rate is %f"%(t_delta,1000/t_delta))