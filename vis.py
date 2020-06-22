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
import devolution as dev
import threshold as ts


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


print(dev.createCell()[15,:,:])


# psf_rw = psf.psfRiWo(rw_args)

# raw = tifffile.imread(os.path.join(sys.path[0],'model_fill/raw.tif'))
# conv = tifffile.imread(os.path.join(sys.path[0],'model_fill/conv.tif'))
# img_0 = tifffile.imread(os.path.join(sys.path[0],'model_snr_fill/snr10_sd2_dec128.tif'))
# img_1 = tifffile.imread(os.path.join(sys.path[0],'model_snr_fill/snr20_sd2_dec128.tif'))
# img_2 = tifffile.imread(os.path.join(sys.path[0],'model_snr_fill/snr50_sd2_dec128.tif'))
# img_3 = tifffile.imread(os.path.join(sys.path[0],'model_snr_fill/snr10_sd2_dec512.tif'))
# img_4 = tifffile.imread(os.path.join(sys.path[0],'model_snr_fill/snr20_sd2_dec512.tif'))
# img_5 = tifffile.imread(os.path.join(sys.path[0],'model_snr_fill/snr50_sd2_dec512.tif'))



# # single image
# ax0 = plt.subplot()
# ax0.imshow(raw[15,:,:])
# slice_0 = ax0.imshow(raw[15,:,:])
# slice_0.set_clim(vmin=0, vmax=4100) 
# divider_0 = make_axes_locatable(ax0)
# cax = divider_0.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_0, cax=cax)
# ax0.axes.xaxis.set_visible(False)
# ax0.axes.yaxis.set_visible(False)



# # middle slices
# max_lim = 1100

# ax0 = plt.subplot(231)
# slice_0 = ax0.imshow(img_0[15,:,:])
# slice_0.set_clim(vmin=0, vmax=max_lim) 
# divider_0 = make_axes_locatable(ax0)
# cax = divider_0.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_0, cax=cax)
# ax0.axes.xaxis.set_visible(False)
# ax0.axes.yaxis.set_visible(False)
# ax0.set_title('SNR 10dB,\n128 iterations')

# ax1 = plt.subplot(232)
# slice_1 = ax1.imshow(img_1[15,:,:])
# slice_1.set_clim(vmin=0, vmax=max_lim) 
# divider_1 = make_axes_locatable(ax1)
# cax = divider_1.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_1, cax=cax)
# ax1.axes.xaxis.set_visible(False)
# ax1.axes.yaxis.set_visible(False)
# ax1.set_title('SNR 20dB,\n128 iterations')

# ax2 = plt.subplot(233)
# slice_2 = ax2.imshow(img_2[15,:,:])
# slice_2.set_clim(vmin=0, vmax=max_lim) 
# divider_2 = make_axes_locatable(ax2)
# cax = divider_2.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_2, cax=cax)
# ax2.axes.xaxis.set_visible(False)
# ax2.axes.yaxis.set_visible(False)
# ax2.set_title('SNR 50dB,\n128 iterations')

# ax3 = plt.subplot(234)
# slice_3 = ax3.imshow(img_3[15,:,:])
# slice_3.set_clim(vmin=0, vmax=max_lim) 
# divider_3 = make_axes_locatable(ax3)
# cax = divider_3.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_3, cax=cax)
# ax3.axes.xaxis.set_visible(False)
# ax3.axes.yaxis.set_visible(False)
# ax3.set_title('SNR 10dB,\n512 iterations')

# ax4 = plt.subplot(235)
# slice_4 = ax4.imshow(img_4[15,:,:])
# slice_4.set_clim(vmin=0, vmax=max_lim) 
# divider_4 = make_axes_locatable(ax4)
# cax = divider_4.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_4, cax=cax)
# ax4.axes.xaxis.set_visible(False)
# ax4.axes.yaxis.set_visible(False)
# ax4.set_title('SNR 20dB,\n512 iterations')

# ax5 = plt.subplot(236)
# slice_5 = ax5.imshow(img_5[15,:,:])
# slice_5.set_clim(vmin=0, vmax=max_lim) 
# divider_5 = make_axes_locatable(ax5)
# cax = divider_5.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_5, cax=cax)
# ax5.axes.xaxis.set_visible(False)
# ax5.axes.yaxis.set_visible(False)
# ax5.set_title('SNR 50dB,\n512 iterations')



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
# ax.voxels(raw, facecolors='blue', edgecolor='k', alpha=.75)
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


# plt.tight_layout()
# plt.show()