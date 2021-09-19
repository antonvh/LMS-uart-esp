# OpenMV Line follower for SPIKE Prime or Robot Inventor
#
# This identifies blue blobs and sends their centroid over uartremote.
# The script assumes you have an LCD addon on your OpenMV Camera.

import sensor, image, time, math,lcd
from uartremote import *

threshold_index = 0 # 0 for red, 1 for green, 2 for blue

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
# This threshold tracks a blue ribbon. Tune it to your line using the OpenMV IDE color graphs
thresholds = [(10,65,-20,35,-65,-20)]

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA2)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(True) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
lcd.init()
clock = time.clock()
ur = UartRemote()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while(True):
    clock.tick()
    img = sensor.snapshot()
    largest_blob_center = []
    largest_blob_size = 0
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200, merge=True):
        # These values depend on the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        #img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        if blob.pixels() > largest_blob_size:
            largest_blob_size = blob.pixels()
            largest_blob_center = [blob.cx(), blob.cy()]
    lcd.display(img)

    if ur.available():
        command, value = ur.receive_command()
        print(largest_blob_center, command, value)
        if command == 'blob':
            ur.ack_ok(command, largest_blob_center)
