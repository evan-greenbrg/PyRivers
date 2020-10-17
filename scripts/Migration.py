import math
import pandas
import numpy
import utm
from scipy import spatial
from matplotlib import pyplot as plt
from scipy import interpolate


def addUTM(df):
    data = {
        'easting': [],
        'northing': [],
        'zone': []
    }
    for idx, row in df.iterrows():
        easting, northing, zone, code = utm.from_latlon(
            row['longitude'], row['latitude']
        )
        data['easting'].append(easting)
        data['northing'].append(northing)
        data['zone'].append(str(zone)+code)

    df['easting'] = data['easting']
    df['northing'] = data['northing']
    df['zone'] = data['zone']

    return df 


def getInterpolateXs(onedf, twodf, length):
    onemin = onedf['easting'].min()
    onemax = onedf['easting'].max()

    twomin = twodf['easting'].min()
    twomax = twodf['easting'].max()

    minx = math.ceil(min([onemin, twomin]))
    maxx = math.ceil(max([onemax, twomax]))

    return numpy.linspace(minx, maxx, length)


def closest(lst, K):
    """
    Finds the closest value in list to value, K
    """
    return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-K))]


def interpolateValues(df, thresh=100, step=1000):

    # Linear length along the line:
    distance = numpy.cumsum(
        numpy.sqrt(numpy.sum(numpy.diff(df, axis=0)**2, axis=1))
    )
    distance = numpy.insert(distance, 0, 0)

    # Find gaps in the centerline
    flags = []
    for i, d in enumerate(distance):
        if i == len(distance)-1:
            continue
        inc = distance[i+1] - d
        if inc > thresh:
            flags.append(i)

    # Divide into multipe interpolation arrays
    dfs = []
    length = 0
    for i, flag in enumerate(flags):
        if i == 0:
            flagdf = df.iloc[1:flag]
            flagdf['distance'] = distance[1:flag]
        else:
            flagdf = df.iloc[flags[i-1]+1:flag]
            flagdf['distance'] = (distance[flags[i-1]+1:flag])

        dfs.append(flagdf)
        length += (flagdf['distance'].iloc[-1] - flagdf['distance'].iloc[0])

    # Interpolate on each centerline section
    interpdf = pandas.DataFrame()
    for section in dfs:
        section['distance'] = section['distance'] / length

        interpolator =  interpolate.interp1d(
            section['distance'], 
            section[['easting', 'northing']], 
            kind='linear', 
            axis=0
        )

        # NEED TO FIND WAY HOW TO SET ALPHA S.T. THERE ARE SAME X VALUES
        alpha = numpy.linspace(
            section['distance'].min(), 
            section['distance'].max(), 
            step
        )
        interpolated_points = pandas.DataFrame(
            interpolator(alpha), 
            columns=['easting', 'northing']
        )
        interpdf = pandas.concat([interpdf, interpolated_points])

    interpdf['easting'] = round(interpdf['easting'], 1)
    interpdf['northing'] = round(interpdf['northing'], 1)

    return interpdf


onep = '/home/greenberg/ExtraSpace/PhD/Projects/BarT/beni/data/1986/beni_1986_data.csv'
twop = '/home/greenberg/ExtraSpace/PhD/Projects/BarT/beni/data/1987/beni_1987_data.csv'

onedf = pandas.read_csv(onep)
twodf = pandas.read_csv(twop)

# Convert one to utm
onedf = addUTM(onedf)
twodf = addUTM(twodf)

# Only use a portion of the dataframe
# I could just have the output to the function be only these two columns
onedf = onedf[['easting', 'northing']]
twodf = twodf[['easting', 'northing']]

# Interpolate values to same x
xs = getInterpolateXs(onedf, twodf, min([len(onedf), len(twodf)]))
onedf = interpolateValues(onedf)
twodf = interpolateValues(twodf)

# WORK TO SAMPLE THE TWO DATAFRAMES S.T THE VALUES ARE THE SAME X

plt.scatter(onedf['easting'], onedf['northing'])
plt.scatter(x, f2(x))
plt.show()


close_points = {
    'easting': [],
    'northing': [],
    'distance': []
}
tree = spatial.KDTree(onedf)
for idx, row in twodf.iterrows():
    distance, neighbors = tree.query(
        [(row['easting'], row['northing'])],
        1
    )
    close_points['easting'].append(onedf.iloc[neighbors[0]]['easting'])
    close_points['northing'].append(onedf.iloc[neighbors[0]]['northing'])
    close_points['distance'].append(distance[0])

close_points = pandas.DataFrame(close_points)

# Filter out points further than threshold
thresh = 20 
close_points = close_points[close_points['distance'] < thresh]


plt.scatter(onedf['easting'], onedf['northing'], s=1, c='red')
plt.scatter(twodf['easting'], twodf['northing'], s=1, c='blue')
plt.scatter(close_points['easting'], close_points['northing'])
plt.show()


