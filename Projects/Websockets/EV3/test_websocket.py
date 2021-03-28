import time
from uartremote import *

u=UartRemote(Port.S1)

t_start=time.time()
for i in range(1000):
    q=u.send_receive('cmd','s','hierpdepiep %i'%i)

t_delta=time.time()-t_start
print("1000 transactions in %fs. Rate is %f"%(t_delta,1000/t_delta))