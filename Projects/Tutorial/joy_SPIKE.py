from projects.uartremote import UartRemote
import hub
import time
hub.display.pixel(0, 0, 9)

ur=UartRemote('D')                 # LMS-ESP32 is connected to port "D", change if otherwise

def plot_pixel(x,y):
    hub.display.clear()
    hub.display.pixel(x,y,9)       # plot pixel @ coordinate (x,y) with intensity 9
    
    
while not hub.button.left.was_pressed():
    ack,joy=ur.call('read_joy')
    x_pixel=joy][0]//52            # joystick value between 0..255, x_pixel = 0..4
    y_pixel=joy[1]//52             # joystick value between 0..255, y_pixel = 0..4
    plot_pixel(4-x_pixel,y_pixel)  # mirror in x directorion: 4 - x_pixel
    time.sleep_ms(50)              # sleep 50ms (~20 loops per second)