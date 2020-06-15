#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Implementation of the global difference stopping criterion
for RL algorithm.

"""

import sys
import os
import logging
from timeit import default_timer as timer

import numpy as np
import pandas as pd
from skimage import util
from skimage.exposure import histogram as hist
from skimage.external import tifffile

from flowdec import data as fd_data
from flowdec import restoration as fd_restoration
from flowdec import psf as fd_psf

sys.path.append('modules')
import devolution as dev

def dec(img, psf, i):
    """ Iterative application of deconvolution.

    """
    # processed_img = ts.backCon(img, 5)  # background extraction
    logger.info('      Deconvolution with {} iteration start'.format(i))
    acq = fd_data.Acquisition(data=img,
                              kernel=psf)
    algo = fd_restoration.RichardsonLucyDeconvolver(n_dims=acq.data.ndim, pad_min=[1, 1, 1]).initialize()
    res = algo.run(acq, niter=i)

    logger.info('      Deconvolution with {} iteration complete'.format(i))
    return res.data

def globDif(img_0, img_1, p=8, max=256):
    hist_0 = hist(img_0)[0]
    hist_1 = hist(img_1)[0]

    


    


FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('DEBUG'))
logger = logging.getLogger('DeconvolutionCLI')


raw_img = tifffile.imread(os.path.join(sys.path[0], 'model_circ/raw.tif'))
conv_img = tifffile.imread(os.path.join(sys.path[0], 'model_circ/conv.tif'))
psf = tifffile.imread(os.path.join(sys.path[0], 'model_circ/psf.tif'))


print(hist(conv_img)[0])