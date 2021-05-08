# Face Detection Example
#
# This example shows off the built-in face detection feature of the OpenMV Cam.
#
# Face detection works by using the Haar Cascade feature detector on an image. A
# Haar Cascade is a series of simple area contrasts checks. For the built-in
# frontalface detector there are 25 stages of checks with each stage having
# hundreds of checks a piece. Haar Cascades run fast because later stages are
# only evaluated if previous stages pass. Additionally, your OpenMV Cam uses
# a data structure called the integral image to quickly execute each area
# contrast check in constant time (the reason for feature detection being
# grayscale only is because of the space requirment for the integral image).

import sensor, time, image
from pyb import UART
from vl53l0x import VL53L0X

# Init rangefinder
try:
    tof = VL53L0X()
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
    tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)
except:
    pass

# Reset sensor
sensor.reset()

# Sensor settings
sensor.set_contrast(3)
sensor.set_gainceiling(16)
# HQVGA and GRAYSCALE are the best for face tracking.
sensor.set_framesize(sensor.HQVGA)
sensor.set_pixformat(sensor.GRAYSCALE)

# Init UART
uart = UART(3, 115200, timeout_char = 1000)
uart.read(500)

# HQVGA = 240x160
H_CENTER = 120
V_CENTER = 80
def center(r):
    return (r[0] + r[2]//2, r[1] + r[3]//2)

def dist_from_center(c):
    return (c[0]-H_CENTER, c[1]-V_CENTER)

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

# FPS clock
clock = time.clock()

while (True):

    request = uart.read(1)
    #print(request)
    if request == b'f':
        # Capture snapshot
        img = sensor.snapshot()

        # Find objects.
        # Note: Lower scale factor scales-down the image more and detects smaller objects.
        # Higher threshold results in a higher detection rate, with more false positives.
        objects = img.find_features(face_cascade, threshold=0.75, scale_factor=1.25)

        # Draw objects
        #for r in objects:
            #img.draw_rectangle(r)
        if objects:
            result = "({:+04d},{:+04d})".format(*dist_from_center(center(objects[0])))
        else:
            result = "(0000,0000)"
        uart.write(result)

    if request == b'r':
        result = 0
        try:
            # Start ranging. Needed?
            tof.start()
            result = (tof.read()-20)/10
            #print(result)
            # Needed?
            tof.stop()
        except:
            pass
        uart.write(str(result))
