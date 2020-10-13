import os
import re
import glob
import math

import pandas
import rasterio
from rasterio import transform
from matplotlib import pyplot as plt


PIXEL_SIZE = 30     # Landsat 30m pixels
YEAR = 1985


def getDataFiles(data_fps):
    """"
    From list of files in directory structure, return data files by type
    """
    data_files = {
        'centerline': [],
        'width': [],
        'curvature': []
    }
    for data_fp in data_fps:
        if re.match(r".*/.*centerline.csv", data_fp):
            data_files['centerline'].append(data_fp)
        if re.match(r".*/.*widths.csv", data_fp):
            data_files['width'].append(data_fp)
        if re.match(r".*/.*curvatures.csv", data_fp):
            data_files['curvature'].append(data_fp)

    return data_files


def buildDataFrame(ds, centerline, width, curvature):
    # Save image data to dataframe
    data = {
        'longitude': [],
        'latitude': [],
        'width': [],
        'curvature': [],
    }
    for idx, row in centerline.iterrows():
        lon, lat = ds.xy(row['row'], row['col'])

        data['longitude'].append(lon)
        data['latitude'].append(lat)
        data['width'].append(width.iloc[idx][0] * PIXEL_SIZE)
        data['curvature'].append(curvature.iloc[idx][0] * PIXEL_SIZE)

    return pandas.DataFrame(data)


def stackAllIdxs(year_dfs):
    """
    Takes the list of dataframes and turns it into a single dataframe
    """
    if len(year_dfs) == 0:
        return year_dfs[0]
    else:
        return pandas.concat(year_dfs).reset_index(drop=True)


# Get Image and data file paths from given year
for year in range(1985, 2001):
    image_root = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/beni/clipped/{year}/*/*.tif'
    data_root = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/beni/data/{year}/*/*.csv'

    # Get image files
    image_fps = glob.glob(image_root)

    # Get data files
    data_fps = glob.glob(data_root)
    data_files = getDataFiles(data_fps)

    year_dfs = []
    for idx, image_fp in enumerate(image_fps):

        # Load the image
        ds = rasterio.open(image_fp)

        # Load the centerline 
        centerline = pandas.read_csv(
            data_files['centerline'][idx]
            , names=['col', 'row']
        )

        # Load the width
        width = pandas.read_csv(
            data_files['width'][idx], 
            names=['width']
        )

        # Load the curvature 
        curvature = pandas.read_csv(
            data_files['curvature'][idx], 
            names=['curvature']
        )
        curvature = curvature.drop([0, 1]).reset_index(drop=True)

        # Find Spacing and resample at width spacing
        spacing = int(round((len(centerline) / len(width)), 0))
        centerline = centerline.iloc[::spacing].reset_index(drop=True)
        curvature = curvature.iloc[::spacing].reset_index(drop=True)

        # Make sure these two dimensions match
        if len(centerline) > len(width):
            centerline = centerline.iloc[:len(width)]
        if len(centerline) > len(curvature):
            centerline = centerline.iloc[:len(curvature)]

        # Build dataframes and append all idxs
        year_dfs.append(buildDataFrame(ds, centerline, width, curvature))

    # Stack the list of dataframes
    data_df = stackAllIdxs(year_dfs)

    outpath = f'/home/greenberg/ExtraSpace/PhD/Projects/BarT/beni/data/{year}/beni_{year}_data.csv'
    data_df.to_csv(outpath)


