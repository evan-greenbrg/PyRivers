import glob
import os

from matplotlib import pyplot as plt
import rasterio
from PyRivers import RivMap 

river = 'beni'
year = 1985
i = 1

rootdir = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/{river}/clean/{year}/idx{i}'
search_c = f'*{year}*clean*.tif'

q = os.path.join(rootdir, search_c)
fps = glob.glob(q)

i = 1
for fp in fps:

    rootdir = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/{river}/clipped/{year}/idx{i}'
    fn_out = f'{river}_{year}__clip.tif'
    opath = os.path.join(rootdir, fn_out)
    print(opath)

    ds = rasterio.open(fp)
    image = ds.read()
    meta = ds.meta.copy()

    image, meta = RivMap.crop_to_mask(ds)
#    image, meta = RivMap.add_buffer(image, meta)
#    image, meta = RivMap.fill_holes(image, meta)

    if not os.path.exists(rootdir):
        os.makedirs(rootdir)

    with rasterio.open(opath, "w", **meta) as dest:
        dest.write(image)

    i += 1

p = '/home/greenberg/ExtraSpace/PhD/Projects/BarT/beni/clipped/1985/idx1/beni_1985__clip.tif'
ds = rasterio.open(p)
data = ds.read(1)

plt.imshow(data)
plt.show()
