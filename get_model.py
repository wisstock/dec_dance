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

wd_path = os.path.join(sys.path[0],'mod/model_bin/')
psf_name = 'psf.tif'
sphere_name = 'raw.tif'
conv_name = 'conv.tif'


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


# # simple binary sphere 
# arr_size = (30,30,30)
# sphere_center = (15,15,15)
# r=10
# sphere = dev.createSphere(arr_size,
#                           sphere_center,
#                           r,
#                           wall=False)  # arr_size,sphere_center, r)
# sphere[sphere == 1] = 4000  # yfp=1100, hpca=150
# sphere = sphere.astype(np.float32)

# model cell
test_size = [500, 500, 500]
lat = 4
axi = 10

cell = dev.createCell(arr_size=test_size,
                       center=[test_size[0]//2, test_size[1]//2, test_size[2]//2],
                       r=test_size[0]//2-100,
                       Im=100, Ic=50, Lm=1)

img = dev.confBin(cell, L=lat, A=axi)

psf_rw = psf.psfRiWo(rw_args)  # generate PSF
psf_norm = psf_rw/np.sum(psf_rw) # normalizing PSF intergral to 1

logging.info('Image size {}'.format(np.shape(img)))
logging.info('PSF size {}'.format(np.shape(psf_norm)))

start_time = timer()
conv_img = convolve(img, psf_norm, mode='constant')
end_time = timer()
logging.info('Convolution complete in {:.3f} seconds'.format(end_time - start_time))

logging.info('Raw image sum intensity {}'.format(np.sum(img)))
logging.info('Convolve image sum intensity {}'.format(np.sum(conv_img)))

tifffile.imsave(os.path.join(wd_path, psf_name), psf_norm)
tifffile.imsave(os.path.join(wd_path, sphere_name), img)
tifffile.imsave(os.path.join(wd_path, conv_name), conv_img)