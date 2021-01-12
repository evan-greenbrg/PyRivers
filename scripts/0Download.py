import os
from google.cloud import storage

from PyRivers import Downloaders


# outroot = '/Volumes/EGG-HD/PhD Documents/Projects/BarT/riverData'
#outroot = '/home/greenberg/ExtraSpace/PhD/Projects/BarT/riverData/'
outroot = '/Users/greenberg/Documents/PHD/Projects/BarT/LinuxFiles/riverData/'
bucket_name = 'earth-engine-rivmap'
river = 'brazos'
stage = 'raw'
years = [2018]

# for year in range(1984, 2022, 2):
for year in years:
# for year in years:
    Downloaders.pullRiverFiles(outroot, bucket_name, river, year, stage)
