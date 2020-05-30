from ppadb.client import Client
from PIL import Image
import numpy
import time

adb = Client(host='127.0.0.1', port=5037)
devices = adb.devices()

if len(devices) == 0:
    print('no devices')
    quit()

device = devices[0]
last_pixels = []

while True:
    print('calculating...')
    image = device.screencap()

    with open('screen.png', 'wb') as f:
        f.write(image)

    image = Image.open('screen.png')
    image = numpy.array(image, dtype=numpy.uint8)

    pixels = [list(i[:3]) for i in image[1730]]

    transitions = []
    ignore = True
    red = False
    first_value = True

    for i, pixel in enumerate(pixels):
        r, g, b = [int(i) for i in pixel]

        if ignore and (r + g + b) != 0:
            continue
        ignore = False

        if first_value and (r + g + b) != 0:
            transitions.append(i)
            first_value = False

        elif red and (r + g + b) != 301:
            red = False
            transitions.append(i)
            continue

        elif not red and (r + g + b) == 301:
            red = True
            transitions.append(i)
            continue

    start, target1, target2 = transitions
    gap = target1 - start
    distance = gap + 1

    print(f'positions: {transitions}')
    print(f'distance from player to wanted position {distance}')

    device.shell(f'input touchscreen swipe 500 500 500 500 {int(distance)}')

    time_to_wait = 5
    print(f'Waiting {time_to_wait} seconds...')
    time.sleep(time_to_wait)
