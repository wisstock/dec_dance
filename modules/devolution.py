#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Functions for model 3D-data generating
and image characterization.

"""

import sys
import os
import logging

import numpy as np
import math


def createSphere(arr_size=[30, 30, 30],
                 center=[15, 15, 15],
                 r=10,
                 wall=False):
    """ Generate binary array with size 'arr_size' with sphere with radius 'r'.
    'center' - sphere center position;
    wall - sphere wall thickness in px,
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