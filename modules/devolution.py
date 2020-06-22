#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Functions for model 3D-data generating
and image characterization.

Require getpsf module.

"""

import sys
import os
import logging

import numpy as np
import numpy.ma as ma
import math
from scipy.ndimage.filters import convolve
from skimage import util
from skimage.external import tifffile


def createSphere(arr_size=[30, 30, 30],
                 center=[15, 15, 15],
                 r=10,
                 wall=1):
    """ Generate array with size 'arr_size' with sphere with radius 'r'.
    'center' - sphere center position;
    wall - sphere wall thickness in px.

    if this parameter is False sphere will be fill.

    """
    coords = np.ogrid[:arr_size[0], :arr_size[1], :arr_size[2]]
    distance = np.sqrt((coords[0] - center[0])**2 + (coords[1]-center[1])**2 + (coords[2]-center[2])**2)

    if wall:
        logging.info('Void sphere with {}px wall and r={}px created '.format(wall, r))
        outer = 1*(distance <= r)
        inner = 1*(distance <= r-wall)
        return outer - inner
    else:
        logging.info('Filled sphere with r={}px created'.format(r))
        return 1*(distance <= r)

def createCell(arr_size=[30, 30, 30],
               center=[15, 15, 15],
               r=10,
               Im=10,
               Lm=1,
               Ic=2,
               bin=False):
    """ Generate array with size 'arr_size' with sphere with radius 'r'.
    'center' - sphere center position;
    wall - sphere wall thickness in px,
    membrane intensity 'Im' and thickness 'Lm',
    and internal space intensity 'Ic'.

    If 'bin' - True sun return binary sphere.

    if this parameter is False sphere will be fill.

    """
    coords = np.ogrid[:arr_size[0], :arr_size[1], :arr_size[2]]
    cell = np.sqrt((coords[0] - center[0])**2 + (coords[1]-center[1])**2 + (coords[2]-center[2])**2)

    logging.info('Void sphere with {}px wall and r={}px created '.format(Lm, r))

    mask_fill = 1*(cell <= r-Lm)
    mask_memb = Im*(cell <= r) - Ic*(cell <= r-Lm)

    # out = distance <= r-2
    # res = ma.masked_array(outer, mask=out, fill_value=0)

    return mask_memb
    
    # if bin:
    #     return outer - inner
    # else:
    #     logging.info('Filled sphere with r={}px created'.format(r))
    #     return 1*(distance <= r)

def relSNR(arr, lim=10, dim=3):
    """ Calculating relative signal-to-noise ratio (in dB) of 2D or 3D image ('dim').
    Requires size (in px, 'lim') of square region for noise SD calculation.

    PSNR = 10lg(max/SD)

    """

    stack = arr[:,:lim,:lim]
    noise_mean = np.mean(stack)
    noise_sd = np.std(stack)


    logging.info('Image peak val={:.3f}'.format(np.max(arr)))
    logging.info('Noise SD={:.3f} in region {}x{}px'.format(noise_sd, lim, lim))
    logging.info('Noise mean={:.3f} in region {}x{}px'.format(noise_mean, lim, lim))

    snr = 10 * math.log10(np.max(arr)/noise_mean)

    logging.info('Image relative SNR = {:.1f}dB'.format(snr))

    return snr, noise_mean, noise_sd

def PSNR(img_1, img_2, img_max=False):
    """ Calculating PSNR.
    img_1 - native image
    img_2 - noisy image

    """

    mse = np.mean((img_1 - img_2)**2)

    if mse == 0:
        return 100

    if not img_max:
        img_max = np.max(img_1)

    psnr = 20 * math.log10(img_max/math.sqrt(mse))
    logging.info('Image PSNR = {:.1f}dB'.format(psnr))

    return psnr


if __name__=="__main__":
  pass


# That's all!