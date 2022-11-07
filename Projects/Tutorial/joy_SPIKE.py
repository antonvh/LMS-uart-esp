from projects.uartremote import UartRemote
import hub
import time
hub.display.pixel(0, 0, 9)

ur=UartRemote('D')

def plot_pixel(x,y):
    hub.display.show(" ")
    hub.display.pixel(x,y,9)
    
    
while not hub.button.left.was_pressed():
    ack,joy=ur.call('read_joy')
    plot_pixel(4-(joy[0]//50)%5,(joy[1]//50)%5)
    time.sleep_ms(50)