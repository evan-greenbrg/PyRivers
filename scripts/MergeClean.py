import glob
import os

from matplotlib import pyplot as plt
import rasterio
from PyRivers import RasterHelpers 

river = 'beni'
year = 1985

rootdir = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/{river}/{year}'
search_c = f'*{year}*.tif'
q = os.path.join(rootdir, search_c)
fps = glob.glob(q)

out = f'{river}_{year}.tif'
outpath = os.path.join(rootdir, out)

RasterHelpers.files_to_mosaic(fps, outpath)

out = f'{river}_{year}_clean1.tif'
clean_outpath = os.path.join(rootdir, out)
RasterHelpers.cleanRaster(outpath, clean_outpath)
