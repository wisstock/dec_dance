#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Generating convolved and noisy model data.
Results are storing in 'model' folder, create it previously!

Poisson-distributed noise - https://www.numerical-tours.com/matlab/denoisingwav_5_data_dependent/

"""

import sys
import os
import logging
from timeit import default_timer as timer

import numpy as np
from scipy.ndimage.filters import convolve
from skimage import util
from skimage.external import tifffile

sys.path.append('modules')
import devolution as dev
import getpsf as psf

FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('INFO'))

wd_path = os.path.join(sys.path[0],'model_fill/')
psf_name = 'psf.tif'
sphere_name = 'raw.tif'
conv_name = 'conv.tif'
noise_name = 'noise.tif'


# model sphere parameters
arr_size = (30,30,30)
sphere_center = (15,15,15)
r=10

# model PSF parameters
rw_args = {'shape': (15, 15),  # number of samples in z and r direction
           'dims': (1.5, 1.5),   # size in z (1.2um*9slices) and r(0.1um*160px) direction in micrometers
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
                          wall=False)  # arr_size,sphere_center, r)
sphere[sphere == 1] = 4000  # yfp=1100, hpca=150
sphere = sphere.astype(np.float32)

psf_rw = psf.psfRiWo(rw_args)  # generate PSF
psf_norm = psf_rw/np.sum(psf_rw) # normalizing PSF intergral to 1

logging.info('Image size {}'.format(np.shape(sphere)))
logging.info('PSF size {}'.format(np.shape(psf_norm)))

start_time = timer()
conv_sphere = convolve(sphere, psf_norm, mode='constant')
end_time = timer()
logging.info('Convolution complete in {:.3f} seconds'.format(end_time - start_time))

noise_sphere = util.random_noise(conv_sphere, mode='gaussian',
                                              mean=190,  # yfp=175, hpca=190
                                              var=14,    # yfp=13, hpca=14
                                              clip=False)

logging.info('Raw image sum intensity {}'.format(np.sum(sphere)))
logging.info('Convolve image sum intensity {}'.format(np.sum(conv_sphere)))

tifffile.imsave(os.path.join(wd_path, psf_name), psf_norm)
tifffile.imsave(os.path.join(wd_path, sphere_name), sphere)
tifffile.imsave(os.path.join(wd_path, conv_name), conv_sphere)
tifffile.imsave(os.path.join(wd_path, noise_name), noise_sphere)