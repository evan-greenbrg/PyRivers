import os
import pickle
import glob
import re

import rasterio
import pandas
from shapely import geometry
import geopandas as gpd
from matplotlib import pyplot as plt
from PyRivers import Width


pattern = '(.*)\/(\w*)\/.*\/(\d{4})\/(\w*)\/'

root = '/Users/greenberg/Documents/PHD/Projects/BarT/RiverData/beni/**'
inname = '*polygon'

inpath = os.path.join(root, inname)
fps = glob.glob(inpath, recursive=True)

test1 = fps[0]
test2 = fps[4]

data = {
    'root': [],
    'river': [],
    'year': [],
    'idx': [],
    'poly': [],
    'fp': [],
}
for fp in fps:
    regex = re.search(pattern, fp)
    data['root'].append(regex.group(1))
    data['river'].append(regex.group(2))
    data['year'].append(regex.group(3))
    data['idx'].append(regex.group(4))
    data['fp'].append(fp)

    with open(fp, "rb") as poly_file:
        data['poly'].append(pickle.load(poly_file))

meta_df = pandas.DataFrame(data)
meta_df = meta_df.sort_values(by='year').reset_index(drop=True)

polys = {}
for idx, row in meta_df.iterrows():
    polys[row['year']] = row['poly']

root = '/Users/greenberg/Documents/PHD/Projects/BarT/RiverData/beni/**'
inname = '*width.csv'
inpath = os.path.join(root, inname)
centerline_fps = glob.glob(inpath, recursive=True)

centerline_data = {
    'root': [],
    'river': [],
    'year': [],
    'idx': [],
    'fp': [],
}
for fp in centerline_fps:
    regex = re.search(pattern, fp)
    centerline_data['root'].append(regex.group(1))
    centerline_data['river'].append(regex.group(2))
    centerline_data['year'].append(regex.group(3))
    centerline_data['idx'].append(regex.group(4))
    centerline_data['fp'].append(fp)
centerline_meta = pandas.DataFrame(
    centerline_data
).sort_values(
    by='year'
).reset_index(drop=True)

centerlines = {}
for idx, row in centerline_meta.iterrows():
    centerlines[row['year']] = pandas.read_csv(row['fp'])

one = polys['1987']
two = polys['1990']
centerline1 = centerlines['1987']
centerline2 = centerlines['1990']

diff = two.difference(one)
fig, axs = plt.subplots(1, 1, sharex=True)

p1 = gpd.GeoSeries(one)
p2 = gpd.GeoSeries(two)
p3 = gpd.GeoSeries(diff)

# p1.plot(color='red', ax=axs)
# p2.plot(color='blue', ax=axs)
p3.plot(color='orange', ax=axs)
axs.scatter(centerline2['coli'], centerline2['rowi'])
axs.scatter(centerline1['coli'], centerline1['rowi'])

plt.show()
