import hub
import time
from mindstorms import Motor
from projects.uartremote import *           # import UartRemote library
motora=Motor('A')                           # connect motot to port "A"
ur=UartRemote('D')                          # LMS-ESP32 is connected to port "D"



while not hub.button.left.was_pressed():
    angle=motora.get_position()             # read absolute angle from motor A
    ack,resp=ur.call('led','repr',angle)    # call function led remotely and pass
                                            # angle as argument
    time.sleep_ms(50)                       # sleep 50ms (loop 20 times per second)