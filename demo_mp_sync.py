#!/usr/bin/env python
import freenect
import matplotlib.pyplot as mp
import frame_convert
import signal
import time
import scipy.io as sio
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches

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

fig = plt.figure(1)
# mp.figure(1)
# image_depth = mp.imshow(get_depth(), interpolation='nearest', animated=True)
ax0 = fig.add_subplot(121)
image_depth = ax0.imshow(get_depth(), interpolation='nearest', animated=True)
# mp.colorbar()
# mp.figure(2)
# image_rgb = mp.imshow(get_video(), interpolation='nearest', animated=True)
ax1 = fig.add_subplot(122)
image_rgb = ax1.imshow(get_video(), interpolation='nearest', animated=True)
# mp.colorbar()
print('Press Ctrl-C in terminal to stop')
signal.signal(signal.SIGINT, handler)
loop = 1
test = 0
while keep_running:
    ######################################################################
    ## Test whether there is a plot from before instance and remove it
    ######################################################################
    if (test == 1):
        patch0.remove()
        patch1.remove()
        l0 = lines0.pop(0)
        l1 = lines1.pop(0)
        l0.remove()
        l1.remove()
    ######################################################################
    ## Read data for depth and rgb
    ######################################################################
    depth = get_depth()
    rgb = get_video()
    ######################################################################
    ## Mean and tolerance values test the depth matrix (if inside True, if not False)
    ######################################################################
    mn = 100
    tol = 30
    test = (abs(depth-mn) <= tol)

    # loc = where(abs(depth-mn) <= tol)


    ######################################################################
    ## For loop to save the location of pixel for each true value
    ######################################################################
    xx = array([])
    yy = array([])

    for ii in range(0, len(test)):
        for jj in range(0, len(test.T)):
            if test[ii,jj]:
                # x = where(test[ii,jj]==True)
                # append(xx, median(x))
                xx = append(xx, ii)
                yy = append(yy, jj)

    ######################################################################
    ## Create rectangle surrounding the object and find its median point
    ######################################################################
    try:
        xmin = min(xx)
        xmax = max(xx)
        ymin = min(yy)
        ymax = max(yy)
    except:
        xmin = 0.0
        xmax = 1.0
        ymin = 0.0
        ymax = 1.0

    verts = [
        (ymin, xmin), # left, bottom
        (ymin, xmax), # left, top
        (ymax, xmax), # right, top
        (ymax, xmin), # right, bottom
        (0., 0.), # ignored
        ]

    codes = [Path.MOVETO,
             Path.LINETO,
             Path.LINETO,
             Path.LINETO,
             Path.CLOSEPOLY,
             ]
    path = Path(verts, codes)

    y0 = median(xx)
    x0 = median(yy)

    # rgb2 = rgb[:, :, 1]
    loop += 1
    sio.savemat('rgb' + str(loop) + '.mat', {'rgb': rgb})
    sio.savemat('depth' + str(loop) + '.mat', {'depth': depth})
    #
    ######################################################################
    ## Plotting depth image
    ######################################################################
    # fig = plt.figure(1)
    ax0 = fig.add_subplot(121)
    # ax0.image_depth.set_data(depth)
    ax0.imshow(depth)
    ax0.set_xlim(0,640)
    ax0.set_ylim(480,0)


    ######################################################################
    ## Plotting middle point and rectangle in depth image
    ######################################################################
    lines0 = ax0.plot(x0,y0, 'go')
    patch0 = patches.PathPatch(path, facecolor='none', lw=2)
    ax0.add_patch(patch0)

    ######################################################################
    ## Plotting rgb image
    ######################################################################
    ax1 = fig.add_subplot(122)
    # ax1.image_rgb.set_data(rgb)
    ax1.imshow(rgb)
    ax1.set_xlim(0,640)
    ax1.set_ylim(480,0)

    ######################################################################
    ## Plotting middle point and rectangle in rgb image
    ######################################################################
    ax1 = fig.add_subplot(122)
    lines1 = ax1.plot(x0,y0, 'go')
    patch1 = patches.PathPatch(path, facecolor='none', lw=2)
    ax1.add_patch(patch1)

    test = 1

    plt.draw()

    # # Update figures
    # mp.figure(1)
    # image_depth.set_data(depth)
    # plot(x0,y0, 'go')
    # xlim(0,640)
    # ylim(480,0)
    # # colorbar()
    # mp.figure(2)
    # image_rgb.set_data(rgb2)
    # plot(x0,y0, 'go')
    # xlim(0,640)
    # ylim(480,0)
    # mp.draw()


    # figure(3)

    plt.waitforbuttonpress(0.01)
    time.sleep(5)

