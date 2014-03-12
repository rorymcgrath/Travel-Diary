#!/usr/bin/env python
import freenect
import matplotlib.pyplot as mp
import frame_convert
import signal
import numpy as np
from pylab import *


keep_running = True


def get_depth():
    return frame_convert.pretty_depth(freenect.sync_get_depth()[0])


def get_video():
    return freenect.sync_get_video()[0]


def handler(signum, frame):
    """Sets up the kill handler, catches SIGINT"""
    global keep_running
    keep_running = False

################################################################################
## Find likelihood of color match (0 = perfect match, 255*sqrt(3) = worst 
## possible match)
################################################################################
def create_false_color(a, b):
  return norm(a - b)

mp.ion()
mp.gray()
mp.figure(1)
image_depth = mp.imshow(get_depth(), interpolation='nearest', animated=True)
mp.figure(2)
image_rgb = mp.imshow(get_video(), interpolation='nearest', animated=True)
################################################################################
## This is the rgb color we want to match
################################################################################
reference_array = np.array([100, 100, 100], dtype='uint8')

print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)

while keep_running:
    mp.figure(1)
    image_depth.set_data(get_depth())
    mp.figure(2)
    rgb = get_video()
    test = np.apply_along_axis(create_false_color, 2, rgb, reference_array)
    image_rgb.set_data(test)
    mp.draw()
    mp.waitforbuttonpress(0.01)
