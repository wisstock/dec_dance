#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Creating demo cell object

Poisson-distributed noise - https://www.numerical-tours.com/matlab/denoisingwav_5_data_dependent/

"""

import sys
import os
import logging

import numpy as np
from scipy import ndimage as ndi
from skimage import util
from skimage import filters
from skimage.external import tifffile

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable


sys.path.append('modules')
import devolution as dev


plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#272b30'
plt.rcParams['image.cmap'] = 'inferno'

FORMAT = "%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s"
logging.basicConfig(level=logging.INFO,
                    format=FORMAT)


img_stack = tifffile.imread(os.path.join(sys.path[0], 'data/yfp/yfp.tif'))
img = img_stack[14,:,:]

cell_roi = [70, 250, 70, 250]
img = img[cell_roi[0]:cell_roi[1], cell_roi[2]:cell_roi[3]]
img_gauss = filters.gaussian(img, sigma=3)

low_val = 0.4
high_val = 0.8

low = low_val*np.max(img_gauss)
high = high_val*np.max(img_gauss)


low = np.clip(low, a_min=None, a_max=high)  # ensure low always below high
mask_low = img_gauss > low
mask_high = img_gauss > high
# Connected components of mask_low
labels_low, num_labels = ndi.label(mask_low)
# Check which connected components contain pixels from mask_high
sums = ndi.sum(mask_high, labels_low, np.arange(num_labels + 1))
connected_to_high = sums > 0
thresholded = connected_to_high[labels_low]


ax0 = plt.subplot()
slice_0 = ax0.imshow(mask_high)
# slice_0.set_clim(vmin=0, vmax=max_lim) 
# divider_0 = make_axes_locatable(ax0)
# cax = divider_0.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_0, cax=cax)
# ax0.axes.xaxis.set_visible(False)
# ax0.axes.yaxis.set_visible(False)
# ax0.set_title('')

plt.tight_layout()
plt.show()