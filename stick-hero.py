#!/usr/bin/env python3

## Requirements
## - adb tool
## - pure-python-adb is required

## Steps
## - Connect android phone to your computer
## - Enable Developer Mode
## - Enable USB Debugging Mode 
## - Update Line 38 with respect to your screen resolution
## - Run Script

from ppadb.client import Client
from PIL import Image
import numpy
import time

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no device attached')
    quit()

device = devices[0]

while True:
    image = device.screencap()

    with open('screen.png', 'wb') as f:
        f.write(image)

    image = Image.open('screen.png')
    image = numpy.array(image, dtype=numpy.uint8)

    # Varies on screen size
    pixels = [list(i[:3]) for i in image[2000]]

    transitions = []
    ignore = True
    black = True

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

        if ignore and (r+g+b) != 0:
            continue

        ignore = False

        if black and (r+g+b) != 0:
            black = not black
            transitions.append(i)
            continue

        if not black and (r+g+b) == 0:
            black = not black
            transitions.append(i)
            continue

    start, target1, target2 = transitions
    gap = target1 - start
    target = target2 - target1
    distance = (gap + target / 2) * .98

    print("transition points: " + str(transitions) + ", distance: " + str(distance))

    device.shell("input touchscreen swipe 500 500 500 500 " + str(int(distance)))

    input("Press Enter to continue...")
