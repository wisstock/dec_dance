#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

SNR experiment

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
    logging.info('Deconvolution with {} iteration start'.format(i))

    processed_img = ts.backCon(img, 5)  # background extraction
    acq = fd_data.Acquisition(data=processed_img,
                              kernel=psf)
    algo = fd_restoration.RichardsonLucyDeconvolver(n_dims=acq.data.ndim, pad_min=[1, 1, 1]).initialize()
    res = algo.run(acq, niter=i)

    logger.info('Deconvolution with {} iteration complete'.format(i))
    return res.data

def iter_save(img, i, noise_val, save_list, path, prefix):
    if i in save_list:
        noise_name = str(noise_val)
        noise_name = noise_name.replace('.', '')
        file_name = '{}_snr_{}_dec_{}.tif'.format(prefix, noise_val, i)
        tifffile.imsave(os.path.join(path, file_name), img)
        logging.info('File {} saved'.format(file_name))
        return
    return


FORMAT = '%(asctime)s| %(levelname)s [%(filename)s: - %(funcName)20s]  %(message)s'
logging.basicConfig(format=FORMAT,
                    level=logging.getLevelName('DEBUG'))
logger = logging.getLogger('DeconvolutionCLI')


output_path = os.path.join(sys.path[0], 'model_snr/')

raw_img = tifffile.imread(os.path.join(sys.path[0], 'model_fill/raw.tif'))
conv_img = tifffile.imread(os.path.join(sys.path[0], 'model_fill/conv.tif'))
psf = tifffile.imread(os.path.join(sys.path[0], 'model_circ/psf.tif'))

noise_list = [-1, -0.5, 0, 0.5, 1, 5, 10, 20, 30]  # init SNR in dB
iter_list = [4, 8, 16, 32, 64, 128]
iter_for_save = [8, 32, 128]

psnr_frame = 15  # frame for PSNR calculation

df = pd.DataFrame(columns=['PSNR', 'init_SNR', 'iter'])

start_time = timer()
for noise_lvl in noise_list:
    logging.info('==> Iteration with {}dB noise level start'.format(noise_lvl))

    noise_mean = np.max(raw_img) / round(10**(noise_lvl/10), 2)

    noise_img = util.random_noise(conv_img, mode='gaussian',
                                            mean=noise_mean,
                                            var=15,
                                            clip=False)

    psnr_0 = dev.PSNR(raw_img, noise_img)

    df = df.append(pd.Series([psnr_0, noise_lvl, 0], index=df.columns),
                   ignore_index=True)

    for i in iter_list:
        dec_img = dec(noise_img, psf, i)
        logging.info('    Deconvolution with {} iterations complete!'.format(i))

        i_psnr = dev.PSNR(raw_img, dec_img)

        df = df.append(pd.Series([i_psnr, noise_lvl, i], index=df.columns),
                       ignore_index=True)

        iter_save(noise_img, i, noise_lvl, iter_for_save, output_path,
                  prefix='conv')
        iter_save(dec_img, i, noise_lvl, iter_for_save, output_path,
                  prefix='dec')


    logging.info('==> Iteration with {}dB noise level complete\n'.format(noise_lvl))
end_time = timer()

df.to_csv(output_path+'snr_res.csv', index=False)

logging.info('Modeling complete in {:.3f} seconds'.format(end_time - start_time))