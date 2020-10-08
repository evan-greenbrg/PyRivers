import os
from google.cloud import storage

from PyRivers import Downloaders


outroot = '/home/greenberg/ExtraSpace/PhD/Projects/BarT'
bucket_name = 'earth-engine-rivmap'
river = 'beni'
year = 1990

Downloaders.pullRiverFiles(outroot, bucket_name, river, year)
