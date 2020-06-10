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
from scipy.ndimage import convolve
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

wd_path = os.path.join(sys.path[0],'/models/')
psf_name = 'model_psf.tif'
sphere_name = 'model_cell.tif'


# model sphere parameters
arr_size = (100,100,100)
sphere_center = (50,50,50)
r=35

# model PSF parameters
rw_args = {'shape': (50, 50),  # number of samples in z and r direction
           'dims': (5, 5),   # size in z (1.2um*9slices) and r(0.1um*160px) direction in micrometers
           'ex_wavelen': 462.0,  # excitation wavelength in nanometers
            'em_wavelen': 492.0,  # emission wavelength in nanometers
            'num_aperture': 1.0,
            'refr_index': 1.333,
            'magnification': 60.0,
            'pinhole_radius': 0.250,  # in mm
            'pinhole_shape': 'round'}



sphere = dev.createSphere(arr_size,
                          sphere_center,
                          r,
                          wall=1)  # arr_size,sphere_center, r)
sphere[sphere == 1] = 1000
sphere = sphere.astype(np.float32)

print(np.max(sphere))

# start_time = timer()
# psf_rw = psf.psfRiWo(rw_args)  # generate PSF
# psf = util.img_as_int(psf_rw)
# conv_sphere = convolve(sphere, psf)
# end_time = timer()
# logger.info('Convolution complete in {:.3f} seconds'.format(end_time - start_time))

noise_sphere = util.random_noise(sphere, mode='gaussian',
                                         mean=1,
                                         var=0.5,
                                         clip=False)


# tifffile.imsave(os.path.join(wd_path, psf_name), psf_rw)
# tifffile.imsave(os.path.join(wd_path, sphere_name), noise_sphere)

# 3D vis
# fig =plt.figure(figsize=(6,6))
# ax = fig.gca(projection='3d')
# ax.voxels(sphere, facecolors='b', edgecolor='k')
# plt.show()

# middle slices
ax0 = plt.subplot(121)
slice_0 = ax0.imshow(sphere[50,:,:]) 
divider_0 = make_axes_locatable(ax0)
cax = divider_0.append_axes("right", size="3%", pad=0.1)
plt.colorbar(slice_0, cax=cax)
ax0.set_title('Raw')

# ax1 = plt.subplot(231)
# slice_1 = ax1.imshow(conv_sphere[50,:,:]) 
# divider_1 = make_axes_locatable(ax1)
# cax = divider_1.append_axes("right", size="3%", pad=0.1)
# plt.colorbar(slice_1, cax=cax)
# ax1.set_title('Convolve')

ax2 = plt.subplot(122)
slice_2 = ax2.imshow(noise_sphere[50,:,:]) 
divider_2 = make_axes_locatable(ax2)
cax = divider_2.append_axes("right", size="3%", pad=0.1)
plt.colorbar(slice_2, cax=cax)
ax2.set_title('Noise')

plt.show()