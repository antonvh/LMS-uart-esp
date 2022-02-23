from projects.uartremote import *
from utime import sleep_ms,ticks_ms,ticks_diff
import time
import hub
u=UartRemote("B")
f=0
t=time.ticks_ms()
i=0
while True:
    try:
        f+=0.1
        #ack,f2=u.call('echo','>if',5,f)
        ack,gp=u.call('gamepad')
        s=int((gp[2]+512)/1024*180)
        ack,se=u.call('servo','>Bi',2,s)
        #time.sleep_ms(1)
        #print(f)
        #time.sleep_ms(50)  # add small delay for stability
        i+=1
        if i==60:
            # show ms per frame
            print(time.ticks_diff(time.ticks_ms(),t)/60.)
            print(gp)
            t=time.ticks_ms()
            i=0
    except KeyboardInterrupt:
        print('interrupted!')
        break
    except:
        print("Error",ack,f)


