#!/usr/bin/env python3

""" Copyright © 2020 Borys Olifirov

Generating model data.
Results are storing in 'mod/model_@name@' folder, create it previously!

Require devolution module.

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

