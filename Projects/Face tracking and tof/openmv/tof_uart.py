# Face Detection XY
# with range finder
# Find the location of a face in the picture
# Send coordinates of face over uart if requested with 'f'
# Send range from rangefinder over uart when requested with 'r'

import sensor, time, image
from pyb import UART
from vl53l0x import VL53L0X

# Init uart
#uart = UART(3, 115200, timeout_char = 1000)

# Init rangefinder
tof = VL53L0X()
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[0], 18)
tof.set_Vcsel_pulse_period(tof.vcsel_period_type[1], 14)


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

def center(r):
    return (r[0] + r[2]//2, r[1] + r[3]//2)

def dist_from_center(c):
    return (c[0]-H_CENTER, c[1]-V_CENTER)

# Load Haar Cascade
# By default this will use all stages, lower satges is faster but less accurate.
face_cascade = image.HaarCascade("frontalface", stages=25)
print(face_cascade)

request = ""
tof.start()
while (True):
    #img = sensor.snapshot()
    # Start ranging. Needed?

    result = tof.read()-20

    print(result)
    # Needed?
    #tof.stop()
