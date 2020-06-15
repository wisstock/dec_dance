#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

SD SNR experiment

"""

import sys
import os
import logging
from timeit import default_timer as timer

import numpy as np
import pandas as pd
from skimage import util
from skimage.external import tifffile

from flowdec import data as fd_data
from flowdec import restoration as fd_restoration
from flowdec import psf as fd_psf

sys.path.append('modules')
import devolution as dev
import threshold as ts


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

def iter_save(img, noise_sd, save_list, path):
    if i in save_list:
        file_name = 'sd{}_dec{}.tif'.format(noise_sd, i)
        tifffile.imsave(os.path.join(path, file_name), img)
        logging.info('File {} saved'.format(file_name))
        return
    return


FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('DEBUG'))
logger = logging.getLogger('DeconvolutionCLI')


output_path = os.path.join(sys.path[0], 'model_sd_circ/')

raw_img = tifffile.imread(os.path.join(sys.path[0], 'model_circ/raw.tif'))
conv_img = tifffile.imread(os.path.join(sys.path[0], 'model_circ/conv.tif'))
psf = tifffile.imread(os.path.join(sys.path[0], 'model_circ/psf.tif'))

noise_mean = 0  # init SNR in dB
sd_list = [25, 20, 18, 15, 13, 10, 5, 2, 1, 0]

iter_list = [8, 16, 32, 64, 128, 256, 512, 1024]
iter_for_save = [8, 64, 128, 512]

init_img_mean = 2000
init_noise_sd = 15

psnr_frame = 15  # frame for PSNR calculation

df = pd.DataFrame(columns=['PSNR', 'init_sd', 'sum', 'iter'])

start_time = timer()
for sd_lvl in sd_list: 
    logging.info('==> Iteration with {}dB noise SD start'.format(sd_lvl))

    noise_sd = init_img_mean / round(10**(sd_lvl/10), 4)

    logging.info('||| Noise mean = {:.2f} and noise SD = {:.2f}'.format(noise_mean, noise_sd))

    noise_img = util.random_noise(conv_img, mode='gaussian',
                                      mean=noise_mean,
                                      var=noise_sd,
                                      clip=False)

    psnr_0 = dev.PSNR(raw_img, noise_img)
  
    df = df.append(pd.Series([psnr_0, sd_lvl, np.sum(noise_img), 0], index=df.columns),
                       ignore_index=True)

    tifffile.imsave(os.path.join(output_path, 'conv_sd{}.tif'.format(sd_lvl)), noise_img)

    for i in iter_list:
        dec_img = dec(noise_img, psf, i)

        i_psnr = dev.PSNR(raw_img, dec_img)

        df = df.append(pd.Series([i_psnr, sd_lvl, np.sum(dec_img), i], index=df.columns),
                           ignore_index=True)

        iter_save(dec_img, sd_lvl, iter_for_save, output_path)

    logging.info('==> Iteration with {}dB noise SD complete\n\n'.format(sd_lvl))
end_time = timer()

df.to_csv(output_path+'sd_res.csv', index=False)

logging.info('Modeling complete in {:.2f} seconds'.format(end_time - start_time))