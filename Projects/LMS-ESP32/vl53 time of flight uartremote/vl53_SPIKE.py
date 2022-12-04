from projects.mpy_robot_tools.uartremote import *
from time import sleep_ms

ur=UartRemote("A") # connect ESP to port A


ur.flush() 		# remove everything
			

# wait some time before sending uartremote commands
sleep_ms(1000)
print(ur.call('echo','s','Echo back from ESP'))


while True:
    print(ur.call('vl53'))
    sleep_ms(100)

