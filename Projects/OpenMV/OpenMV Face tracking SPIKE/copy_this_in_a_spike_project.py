# Make sure to install the uartremote library with the SPIKE install script
# Also copy the library on the Flash drive of the OpenMV cam
# Also copy the main.py file in the Library/Micropython/H7 to that flash drive to
# enable the REPL on the UART port.

# TODO: Fix the 20% packet loss on the uart line. Maybe higher baud rate?
# TODO: Increase the framerate
# TODO: Create an inverse solution where the OpenMV camera is the boss.

MAINPY="""
# Face Detection Uartremote Example

import sensor, image
from uartremote import *
ur = UartRemote()

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(3)
sensor.set_gainceiling(16)
# HQVGA and GRAYSCALE are the best for face tracking.
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

# HQVGA = 240x160
H_CENTER = 120
V_CENTER = 80

def location(r):
    # Returns a tuple with the centre of the face detection rectangle
    # Coordinates have sensor centre as 0,0 instead of top left
    c = (r[0] + r[2]//2, r[1] + r[3]//2)
    return (c[0]-H_CENTER, c[1]-V_CENTER)

# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)

def get_face_loc():
    img = sensor.snapshot()

    # Note: Lower scale factor scales-down the image more and detects smaller objects.
    # Higher threshold results in a higher detection rate, with more false positives.
    objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

    if objects:
        return location(objects[0])
    else:
        return (0,0)

# Two signed bytes should be enough for values between -120 and 120
ur.add_command(get_face_loc, 'bb')

# ur.loop()
"""

from projects.uartremote import *
ur = UartRemote('F')
print("UartRemote Library initialized")

ur.repl_activate()
print(ur.repl_run("print('Repl Tested')", raw_paste=False))

print(ur.repl_run(MAINPY))
print("Downloaded script")

ur.repl_run("ur.loop()", reply=False, raw_paste=False)
print("Entered remote listening loop")
ur.flush()

# Constants
DEG_P_PX = 0.27
SPEED = 80 # %

# Init variables & motors
n=0
e=0
i=0


from spike import PrimeHub
myhub = PrimeHub()
lm = myhub.light_matrix
elevation = hub.port.C.motor
left_wheel = hub.port.A.motor
right_wheel = hub.port.B.motor

def sign(n):
    if n:
        return int(abs(n)/n)
    else:
        return n

while True:
    ack, loc = ur.call('get_face_loc')
    if ack != 'err':
        n+=1
        x,y=loc
        if x: 
            lm.show_image('HAPPY')
        base_rotation = int( DEG_P_PX * x )
        wheel_rotation = int( base_rotation * -1.5)
        base_tilt = int( DEG_P_PX * y )

        
        left_wheel.run_for_degrees(wheel_rotation, SPEED * sign(wheel_rotation))
        right_wheel.run_for_degrees(wheel_rotation, SPEED * sign(wheel_rotation))
        elevation.run_for_degrees(base_tilt, SPEED * sign(base_tilt))
    else:
        lm.show_image('SAD')
        e+=1
    if i >50:
        print("Percent of commands lost:{:.0f}".format(e/i*100))
        e=n=i=0
    i+=1

raise SystemExit