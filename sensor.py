import matplotlib
matplotlib.use('Agg')
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import math

df = pd.read_csv('sensordata.csv', skiprows=0, sep=',')

# total number of rows
row = df.shape[0]
# total number of columns
col = df.shape[1]

#calculate number of stops
stopped = False
number_of_stops = 0
for i in range(0, row):
    if df.iloc[i][27] == 0 and stopped:
        continue
    elif df.iloc[i][27] == 0:
        number_of_stops += 1
        stopped = True
    else:
        stopped = False

# approximate radius of earth in km
R = 6373.0
# total cumulative distance
distance = 0
# each distance between 2 pairs of coordinates
distances = []

for i in range(0, row-1):
    # algorithm taken from: https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
    lat1 = math.radians(df.iloc[i][22])
    lon1 = math.radians(df.iloc[i][23])
    lat2 = math.radians(df.iloc[i+1][22])
    lon2 = math.radians(df.iloc[i+1][23])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

    distance += R * c
    distances.append(distance * .621371)

time = df.iloc[row-1][col-2]
average_speed = df.iloc[:,27].mean()
max_speed = df.iloc[:,27].max()
print ('\nTotal time: ' + str((time/(1000*60)%60)) + ' minutes')
print ('Average speed: ' + str(average_speed) + ' km/h or ' +  str(average_speed * .621371) + ' mph')
print ('Max speed: ' + str(max_speed) + ' km/h or ' + str(max_speed * .621371) + ' mph')
print ('Number of stops: ' + str(number_of_stops))
print ('Distance travelled: ' + str(distance) + ' km or ' + str(distance * .621371) + ' miles\n')

# fix y label
plt.plot(distances)
plt.ylabel('Cumulative Distance (miles)')
plt.xlabel('Number of distances calculated from long. and lat.')
out_png = 'distances.png'
plt.savefig(out_png, dpi=150)
plt.clf()

# average and max speed and speeds and stops
plt.plot(df.iloc[:,27])
plt.axhline(average_speed, color='r', linestyle='dashed', linewidth=2)
plt.axhline(max_speed, color='g', linestyle='dashed', linewidth=2)
plt.ylabel('km/h')
plt.xlabel('number of entries')
plt.legend(['speeds', 'average speed', 'max speed'], loc='upper left')
out_png = 'speed.png'
plt.savefig(out_png, dpi=150)
plt.clf()