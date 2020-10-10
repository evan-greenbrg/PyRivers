pasimport glob
import os

from matplotlib import pyplot as plt
import rasterio
from PyRivers import RasterHelpers 

river = 'beni'
year = 2001
i = 1

rootdir = f'/Volumes/EGG-HD/PhD Documents/Projects/BarT/riverData/{river}/raw/{year}'
# rootdir = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/{river}/raw/{year}'
search_c = f'*{year}*.tif'
q = os.path.join(rootdir, search_c)
fps = glob.glob(q)

out = f'{river}_{year}.tif'
outpath = os.path.join(rootdir, out)

RasterHelpers.files_to_mosaic(fps, outpath)

out = f'{river}_{year}_clean.tif'
rootdir = f'/Volumes/EGG-HD/PhD Documents/Projects/BarT/riverData/{river}/clean/{year}/idx{i}'
# rootdir = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/{river}/clean/{year}/idx{i}'
clean_outpath = os.path.join(rootdir, out)

# Check if path exists
if not os.path.exists(rootdir):
    os.makedirs(rootdir)

RasterHelpers.cleanRaster(outpath, clean_outpath)

