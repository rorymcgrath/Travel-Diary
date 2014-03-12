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
reference_array = np.array([255,128,0])


################################################################################
## Create a mask image of the color of interest. In this case safety orange.
################################################################################
ref_matrix = np.zeros((480, 640, 3), dtype=uint8)
for i in xrange(0,480):
  for j in xrange(0,640):
    ref_matrix[i][j][0] = 232
    ref_matrix[i][j][1] = 118
    ref_matrix[i][j][2] = 0


while keep_running:
    mp.figure(1)
    data = get_video()
   
    ## Get the image from the camera
    image_depth.set_data(get_depth())
    mp.figure(2)

    ## Find the difference between the camera image and the mask image
    falseImage = np.sum(np.abs(np.subtract(ref_matrix.astype(int),data.astype(int))),axis=2).astype(uint8)
   
    ## Convert to black white image. The threshold here is currently set to 100.
    falseImage[falseImage > 100] = 255
    falseImage[falseImage < 101] = 0

    ## Remove spurs from the data
    falseImage = ndimage.binary_opening(falseImage)
    falseImage = ndimage.binary_closing(falseImage).astype(uint8)
    
    ## Further clean image by applying Gaussian filter
    falseImage = ndimage.gaussian_filter(falseImage, sigma=1/(2.0))
    
    ## Label all blobs in the image
    label_im, nb_labels = ndimage.label(falseImage)
    sizes = ndimage.sum(falseImage,label_im,range(nb_labels+1))
    
    ## Remove all blobs that have a surface area less than 1000 pixels
    mask_size = sizes < max(sizes)
    max_id = max(enumerate(sizes),key=lambda x: x[1])[0]
    mask_size = sizes < 1000
    remove_pixel = mask_size[label_im]
    
    ## Find the main object in the scene. This is the larges blob.
    main_object = sizes < max(sizes)-1
    get_pixels = main_object[label_im]
    label_im[remove_pixel] = 0
    data[get_pixels] = [0,0,0]
    
    ## Highlight main object in rgb 
    label_im[label_im > 0] = 255
    label_im[label_im < 100] = 0
    
    ## Find center of mass of the principle object and draw a green square
    com = ndimage.measurements.center_of_mass(data,max_id)
    data[get_pixels] = [255,255,255]
    for i in xrange(-5,5):
      for j in xrange(-5,5):
        data[i+com[0]][j+com[1]] = [51,255,51]
    
    ## Display the resulting image
    image_rgb.set_data(data)
    mp.draw()
    mp.waitforbuttonpress(0.1)
