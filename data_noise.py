#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Experimental data characteristic vis

"""

import sys
import os
import logging
from timeit import default_timer as timer

import numpy as np
from scipy.ndimage import convolve
from skimage import util
from skimage.external import tifffile

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable

sys.path.append('modules')
import devolution as dev


FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('INFO'))

plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#272b30'
plt.rcParams['image.cmap'] = 'inferno'

hpca_path = os.path.join(sys.path[0], 'data/hpca_dec_4.tif')
# data_path = os.path.join(sys.path[0], 'data/hpca/hpca.tif')
yfp_path = os.path.join(sys.path[0], 'data/yfp/yfp.tif')

frame = 10
roi_start = [140, 200]  # [85, 150]
roi_lim = 50


hpca_stack = tifffile.imread(hpca_path)
hpca_img = hpca_stack[frame,:,:]
hpca_roi = hpca_img[roi_start[1]:roi_start[1]+roi_lim,roi_start[0]:roi_start[0]+roi_lim]
yfp_stack = tifffile.imread(yfp_path)
yfp_img = yfp_stack[frame,:,:]
yfp_roi = yfp_img[roi_start[1]:roi_start[1]+roi_lim,roi_start[0]:roi_start[0]+roi_lim]


mean, sd = dev.getPSNR(yfp_stack)

# merge_roi = np.dstack((hpca_img, yfp_img,  np.zeros(shape=(320,320))))

# ax0 = plt.subplot()
# ax0.imshow(hpca_roi, cmap='Reds', alpha=1)
# ax0.imshow(yfp_roi, cmap='Blues', alpha=0.7)
# ax0.set_title('Full image')

# plt.tight_layout()
# plt.show()
