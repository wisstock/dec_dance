#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Data visualisation fun.

"""

import sys
import os
import logging

import numpy as np
from skimage.external import tifffile

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

sys.path.append('modules')
import getpsf as psf


FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('INFO'))

plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#272b30'
plt.rcParams['image.cmap'] = 'inferno'

rw_args = {'shape': (50, 50),  # number of samples in z and r direction
           'dims': (1, 1),   # size in z and r direction in micrometers
           'ex_wavelen': 462.0,  # excitation wavelength in nanometers
            'em_wavelen': 492.0,  # emission wavelength in nanometers
            'num_aperture': 1.0,
            'refr_index': 1.333,
            'magnification': 60.0,
            'pinhole_radius': 0.250,  # in mm
            'pinhole_shape': 'round'}

# psf_rw = psf.psfRiWo(rw_args)


data_path = os.path.join(sys.path[0],'model_fill/noise.tif')
# data_path = os.path.join(sys.path[0],'model_fill/dec/dec_128.tif')

img = tifffile.imread(data_path)



ax0 = plt.subplot()
slice0 = ax0.imshow(img[15,:,:])
slice0.set_clim(vmin=0, vmax=650)  # 4200 for circ, 650 for fill
divider0 = make_axes_locatable(ax0)
cax = divider0.append_axes("right", size="3%", pad=0.1)
plt.colorbar(slice0, cax=cax)



# # 3D vis of binary data
# colors = np.empty(psf_rw.shape, dtype=np.float32)
# alpha = .5
# colors[psf_rw >= .5] = 'red'  # [1, 0, 0, alpha]
# colors[psf_rw < 0.5] = 'blue'  # [0, 1, 0, alpha]
# # colors[2] = [0, 0, 1, alpha]
# # colors[3] = [1, 1, 0, alpha]
# # colors[4] = [0, 1, 1, alpha]
# fig =plt.figure(figsize=(6,6))
# ax = fig.gca(projection='3d')
# ax.voxels(psf_rw, facecolors=colors, edgecolor='k')
# plt.show()

# # demo PSF
# ax_xz = plt.subplot(121)
# slice_xz = ax_xz.imshow(psf_rw[:,50,:], cmap='nipy_spectral')  # 
# divider_xz = make_axes_locatable(ax_xz)
# cax = divider_xz.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_xz, cax=cax)
# ax_xz.set_title('X-Z')

# ax_xy = plt.subplot(122)
# slice_xy = ax_xy.imshow(psf_rw[50,:,:], cmap='nipy_spectral')  # 
# divider_xy = make_axes_locatable(ax_xy)
# cax = divider_xy.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_xy, cax=cax)
# ax_xy.set_title('X-Y')


plt.tight_layout()
plt.show()