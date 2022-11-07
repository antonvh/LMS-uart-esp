import hub
import time
from mindstorms import Motor
from projects.uartremote import *
motora=Motor('A')
ur=UartRemote('D')



while not hub.button.left.was_pressed():
    angle=motora.get_position()
    ack,resp=ur.call('led','repr',angle)
    time.sleep_ms(50)