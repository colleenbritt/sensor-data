'''
A program that extracts information from the data gathered
from AndroSenser.

Python 3.6
'''

import matplotlib
matplotlib.use('Agg')
import pandas as pd
import matplotlib.pyplot as plt
import math

'''
Calculates the number of stops that occurred.
'''
def calculate_stops(df, row):
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
    return number_of_stops

'''
Calcuates the total distance travelled.
'''
def calculate_total_distance(df, row):
    # approximate radius of earth in km
    R = 6373.0

    distance = 0

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
        
    return distance

'''
Calculates each distance between 2 pairs of longitude and
latitude coordinates.
'''
def calculate_distances(df, row):
    distances = []
    distance = 0

    # approximate radius of earth in km
    R = 6373.0

    for i in range(0, row-1):
        # algorithm taken from: 
        # https://stackoverflow.com/questions/19412462/getting-distance-between-two-points-based-on-latitude-longitude
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

    return distances

'''
Prints the features that were calculated.
'''
def print_features(df, row, col, time, average_speed, max_speed, number_of_stops, distance, average_light):
    
    print ('\nTotal time: ' + str((time/(1000*60)%60)) + ' minutes')
    print ('Average speed: ' + str(average_speed) + ' km/h or ' +  str(average_speed * .621371) + ' mph')
    print ('Max speed: ' + str(max_speed) + ' km/h or ' + str(max_speed * .621371) + ' mph')
    print ('Number of stops: ' + str(number_of_stops))
    print ('Distance travelled: ' + str(distance) + ' km or ' + str(distance * .621371) + ' miles')
    print ('Average Light: ' + str(average_light) + " lux\n")

'''
Creates a graph of the distances between each pair of latitude
and longitude coordinates. It is saved to a .png file.
'''
def plot_distance(distances):
    plt.plot(distances)
    plt.ylabel('Cumulative Distance (miles)')
    plt.xlabel('Number of distances calculated from long. and lat.')
    out_png = 'distances.png'
    plt.savefig(out_png, dpi=150)
    plt.clf()

'''
Creates a graph of the average light amount and compares it
to all of the entries of the light data. It is saved to a .png
file.
'''
def plot_light(df, average_light):
    plt.plot(df.iloc[:,12])
    plt.axhline(average_light, color='r', linestyle='dashed', linewidth=2)
    plt.ylabel('Lux')
    plt.xlabel('Number of entries')
    out_png = 'light.png'
    plt.savefig(out_png, dpi=150)
    plt.clf()

'''
Creates a graph of the average and max speeds and compares them
to the all of the entries of the speed data. It is saved to a
.png file.
'''
def plot_speed(df, average_speed, max_speed):
    plt.plot(df.iloc[:,27])
    plt.axhline(average_speed, color='r', linestyle='dashed', linewidth=2)
    plt.axhline(max_speed, color='g', linestyle='dashed', linewidth=2)
    plt.ylabel('km/h')
    plt.xlabel('Number of entries')
    plt.legend(['speeds', 'average speed', 'max speed'], loc='upper left')
    out_png = 'speed.png'
    plt.savefig(out_png, dpi=150)
    plt.clf()

'''
Main function. Reads data from .cvs file and calls other function to
extract information.
'''
def main():
    df = pd.read_csv('sensordata.csv', skiprows=0, sep=',')

    # total number of rows
    row = df.shape[0]
    # total number of columns
    col = df.shape[1]
    # column containing speed data
    speed = df.iloc[:,27]
    # column containing light data
    light = df.iloc[:,12]

    # gets the total time from the specific entry in .csv file
    time = df.iloc[row-1][col-2]
    # calculates average speed
    average_speed = speed.mean()
    # calculates max speed
    max_speed = speed.max()
    # calculates average light
    average_light = light.mean()
    # total number of stops
    number_of_stops = calculate_stops(df, row)
    # array of distances between pairs of longitude and latitude coordinates
    distances = calculate_distances(df, row)
    # total distance travelled
    distance = calculate_total_distance(df, row)

    print_features(df, row, col, time, average_speed, max_speed, number_of_stops, distance, average_light)

if __name__ == "__main__":
    main()