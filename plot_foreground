import scipy.io as sio
from pylab import *
import matplotlib.pyplot as plt
from matplotlib.path import Path
import matplotlib.patches as patches


depth = sio.loadmat('depth.mat')
depth = depth['depth']
rgb = sio.loadmat('rgb.mat')
rgb = rgb['rgb']

rgb2 = rgb[:, :, 1]
# d = depth[146,93]
# print d
# figure(1)
# imshow(depth)
# colorbar()
# colormaps()
# # show()

mn = 100
tol = 50

# red is true, blue is false. True is one and false is zero

test = (abs(depth-mn) <= tol)
xx = array([])
yy = array([])

for ii in range(0, len(test)):
    for jj in range(0, len(test.T)):
        if test[ii,jj]:
            # x = where(test[ii,jj]==True)
            # append(xx, median(x))
            xx = append(xx, ii)
            yy = append(yy, jj)


xmin = min(xx)
xmax = max(xx)
ymin = min(yy)
ymax = max(yy)

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

print(xmin, xmax, ymin, ymax)
y0 = median(xx)
x0 = median(yy)


## Plotting depth image
fig = plt.figure(1)
ax0 = fig.add_subplot(121)
ax0.imshow(depth)
ax0.set_xlim(0,640)
ax0.set_ylim(480,0)


# Plotting median point on depth image
# ax1 = fig.add_subplot(121)
lines0 = ax0.plot(x0,y0, 'go')

# Plotting rectangle on depth image
patch0 = patches.PathPatch(path, facecolor='none', lw=2)
ax0.add_patch(patch0)

# Adding second subplot for RGP
ax1 = fig.add_subplot(122)
ax1.imshow(rgb)
ax1.set_xlim(0,640)
ax1.set_ylim(480,0)

# # Adding point and rectangle for RGP plot
ax1 = fig.add_subplot(122)
lines1 = ax1.plot(x0,y0, 'go')
patch1 = patches.PathPatch(path, facecolor='none', lw=2)
ax1.add_patch(patch1)

#remove dots and squares
# patch0.remove()
# patch1.remove()
# l0 = lines0.pop(0)
# l1 = lines1.pop(0)
# l0.remove()
# l1.remove()
#
#
#
# ax1.plot(x0+10,y0+10, 'go')

plt.show()


# figure(2)
# imshow(rgb)
# plot(x0,y0, 'go')
# xlim(0,640)
# ylim(480,0)
# colorbar()
# show()
