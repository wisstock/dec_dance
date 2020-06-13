#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Deconvolution of model data

"""

import sys
import os
import logging

import numpy as np
from timeit import default_timer as timer
from skimage import io
# from skimage.external import tifffile

from flowdec import data as fd_data
from flowdec import restoration as fd_restoration
from flowdec import psf as fd_psf

sys.path.append('modules')
import threshold as ts
import getpsf as psf


FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('DEBUG'))
logger = logging.getLogger('DeconvolutionCLI')

input_path = os.path.join(sys.path[0], 'model_fill/noise.tif')
output_path = os.path.join(sys.path[0], 'model_fill/dec/')

psf_path = os.path.join(sys.path[0], 'model_fill/psf.tif')

iter_list = [4, 8, 16, 32, 64, 128]

scaling_factor = 5  # subtraction region part for background calculation

img = io.imread(input_path)
logger.info('File "{}" uploaded'.format(input_path.split('/')[-1]))

for n_iter in iter_list:
    logging.info('Deconvolution with {} iteration starting'.format(n_iter))
    start_time = timer()

    processed_img = ts.backCon(img, np.shape(img)[1] // scaling_factor)  # background extraction

    psf_rw = io.imread(psf_path)

    acq = fd_data.Acquisition(data=processed_img,
                              kernel=psf_rw)

    logger.debug('Loaded data with shape {} and psf with shape {}'.format(acq.data.shape, acq.kernel.shape))

    algo = fd_restoration.RichardsonLucyDeconvolver(n_dims=acq.data.ndim, pad_min=[1, 1, 1]).initialize()
    res = algo.run(acq, niter=n_iter)

    output_name = 'dec_%s.tif' % (n_iter)
    io.imsave(os.path.join(output_path, output_name), res.data)

    logger.info('Deconvolution with {} iteration complete'.format(n_iter))


end_time = timer()
logger.info('Deconvolution complete in {:.3f} seconds'.format(end_time - start_time))
