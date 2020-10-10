import os
from google.cloud import storage

from PyRivers import Downloaders


outroot = '/Volumes/EGG-HD/PhD Documents/Projects/BarT/riverData'
bucket_name = 'earth-engine-rivmap'
river = 'beni'
year = 1985

for year in range(1986, 2001):
    Downloaders.pullRiverFiles(outroot, bucket_name, river, year)
