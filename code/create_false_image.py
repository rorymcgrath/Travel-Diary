#!/usr/bin/env python
import freenect
import matplotlib.pyplot as mp
import frame_convert
import signal
import numpy as np
import itertools
from pylab import *
from scipy import ndimage

keep_running = True


def get_depth():
    return frame_convert.pretty_depth(freenect.sync_get_depth()[0])

def get_video():
    return freenect.sync_get_video()[0]

def handler(signum, frame):
    """Sets up the kill handler, catches SIGINT"""
    global keep_running
    keep_running = False

mp.ion()
mp.gray()
mp.figure(1)
image_depth = mp.imshow(get_depth(), interpolation='nearest', animated=True)
mp.figure(2)
image_rgb = mp.imshow(get_video(), interpolation='nearest', animated=True)
mp.colorbar()
print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)

## Create a mask image with color to detech
ref_matrix = np.zeros((480, 640, 3), dtype=uint8)
for i in xrange(0,480):
  for j in xrange(0,640):
    ref_matrix[i][j][0] = 232
    ref_matrix[i][j][1] = 118
    ref_matrix[i][j][2] = 0

while keep_running:
    mp.figure(1)
    ## Get image from camera
    data = get_video()
    image_depth.set_data(get_depth())
    mp.figure(2)
    ## Create the false image
    falseImage = np.sum(np.abs(np.subtract(ref_matrix.astype(int),data.astype(int))),axis=2).astype(uint8)
    image_rgb.set_data(falseImage)
    mp.draw()
    mp.waitforbuttonpress(0.1)
