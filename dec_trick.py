#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Experiments with convolution and deconvolution.
Require 'devolution' module.

"""

import sys
import os
import logging
from timeit import default_timer as timer

import numpy as np
from scipy.ndimage import convolve
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable

from mpl_toolkits.mplot3d import Axes3D

sys.path.append('modules')
import devolution as dev



arr_size = (100,100,100)
sphere_center = (50,50,50)
r=10
sphere = dev.createSphere(wall=1)  # arr_size,sphere_center, r)


print(sphere[15,:,:])

# 3D vis
# fig =plt.figure(figsize=(6,6))
# ax = fig.gca(projection='3d')
# ax.voxels(sphere, facecolors='b', edgecolor='k')
# plt.show()

# # middle slice
# img = sphere[sphere_center[0] // 2,:,:]
# fig, ax = plt.subplots()
# ax.imshow(img)
# plt.show()