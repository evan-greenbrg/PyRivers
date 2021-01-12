import copy
import glob
import os

from matplotlib import pyplot as plt
from matplotlib.widgets import Button
from matplotlib.patches import Rectangle
import numpy as np
import rasterio
from rasterio.merge import merge


def BarIndex(vals, max_vals):
    """
    Discriminating index for identifying water
    """
    return np.sum(vals) / np.sum(max_vals)


def CreateBarMask(image):
    # Calculate index over image
    image = image.transpose()
    index_image = np.zeros((image.shape[0], image.shape[1]))

    # Find Max for each band
    band_max = {}
    for i in range(0,len(image[0, 0 , :])):
        band = image[:, :, i]
        band_max[i] = np.quantile(band[band>0], 0.9)

    # Calculate the index
    for i, row in enumerate(image):
        for j, vals in enumerate(row):
            if vals[0] > 0:
                index_image[i, j] = BarIndex(
                    vals, list(band_max.values())
                )
            else:
                index_image[i, j] = None


    # convert to binrary
    thresh = 1.3
    mask = index_image
    mask[mask < thresh] = 0 
    mask[mask > thresh] = 1 

    # Combine the two masks
#    mask = mask[:,:,0]

    return mask.reshape((
        mask.shape[0],
        mask.shape[1],
        1
    )).transpose()


