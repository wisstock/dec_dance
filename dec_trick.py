#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Experiments with convolution and deconvolution.
Require 'devolution' module.

Poisson-distributed noise - https://www.numerical-tours.com/matlab/denoisingwav_5_data_dependent/

"""

import sys
import os
import logging
from timeit import default_timer as timer

import numpy as np
from skimage import util
from skimage.external import tifffile

import matplotlib
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as patches
from mpl_toolkits.axes_grid1 import make_axes_locatable
from mpl_toolkits.mplot3d import Axes3D

sys.path.append('modules')
import devolution as dev
import getpsf as psf

FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('INFO'))

plt.style.use('dark_background')
plt.rcParams['figure.facecolor'] = '#272b30'
plt.rcParams['image.cmap'] = 'inferno'

wd_path = os.path.join(sys.path[0],'model_circ/')
psf_name = 'psf.tif'
sphere_name = 'raw.tif'
conv_name = 'conv.tif'
noise_name = 'noise.tif'


psf = tifffile.imread(os.path.join(wd_path, psf_name))
raw_sphere = tifffile.imread(os.path.join(wd_path, sphere_name))
conv_sphere = tifffile.imread(os.path.join(wd_path, conv_name))
noise_sphere = tifffile.imread(os.path.join(wd_path, noise_name))


# snr, mean, sd = dev.relSNR(noise_sphere, lim=5)

noise_img = util.random_noise(raw_sphere, mode='gaussian',
                              mean=2000,
                              var=15,
                              clip=False)

psnr = dev.PSNR(raw_sphere, noise_img)


# # 3D vis of binary data
# fig =plt.figure(figsize=(6,6))
# ax = fig.gca(projection='3d')
# ax.voxels(noise_sphere, facecolors='b', edgecolor='k')
# plt.show()

# # middle slices
# ax0 = plt.subplot(231)
# slice_0 = ax0.imshow(raw_sphere[15,:,:])
# slice_0.set_clim(vmin=0, vmax=4200) 
# divider_0 = make_axes_locatable(ax0)
# cax = divider_0.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_0, cax=cax)
# ax0.set_title('Raw')

# ax1 = plt.subplot(232)
# slice_1 = ax1.imshow(conv_sphere[15,:,:])
# slice_1.set_clim(vmin=0, vmax=4200)  
# divider_1 = make_axes_locatable(ax1)
# cax = divider_1.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_1, cax=cax)
# ax1.set_title('Convolve')

# ax2 = plt.subplot(233)
# slice_2 = ax2.imshow(noise_sphere[15,:,:])
# slice_2.set_clim(vmin=0, vmax=4200)  
# divider_2 = make_axes_locatable(ax2)
# cax = divider_2.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_2, cax=cax)
# ax2.set_title('Noise')

# ax3 = plt.subplot(235)
# slice_3 = ax3.imshow(psf[:,15,:], cmap='nipy_spectral') 
# divider_3 = make_axes_locatable(ax3)
# cax = divider_3.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_3, cax=cax)
# ax3.set_title('PSF')

# plt.tight_layout()
# plt.show()