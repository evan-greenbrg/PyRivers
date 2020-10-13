import os
from google.cloud import storage

from PyRivers import Downloaders


# outroot = '/Volumes/EGG-HD/PhD Documents/Projects/BarT/riverData'
outroot = '/home/greenberg/ExtraSpace/PhD/Projects/BarT/'
bucket_name = 'earth-engine-rivmap'
river = 'beni'
stage = 'raw'
year = 1985

for year in range(1985, 2001):
    Downloaders.pullRiverFiles(outroot, bucket_name, river, stage, year)
