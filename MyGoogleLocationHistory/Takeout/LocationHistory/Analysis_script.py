#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
import pandas as pd
import json
from datetime import datetime as dt

phone_off_threshold = 3600*1

with open("Location History.json") as f:
    x = json.load(f)
    data = x["locations"]

def get_time(timepoint):
    ts = int(timepoint['timestampMs'])/1000
    dt_object = dt.fromtimestamp(ts)
    return dt_object


def square_out_datapoints(datalist, minlat, maxlat, minlong, maxlong):
    square = []
    for d in datalist:
        lat = d["latitudeE7"]
        "latitudeE7"
        lon = d["longitudeE7"]
        if (minlat<=lat<=maxlat) and (minlong<=lon<=maxlong):
            square.append(d)
    return square

new_house = []
for d in data:
    dt_obj=get_time(d)
    if (dt_obj.year==2019):
        if (dt_obj.month>6):
            new_house.append(d)
        elif(dt_obj.month==6):
            if (dt_obj.day>=10):
                new_house.append(d)

gymmaxlat, gymminlong = ary(ary([51.674563, -1.287730])*1E7, dtype=int)
gymminlat, gymmaxlong = ary(ary([51.673861, -1.286625])*1E7, dtype=int)
gym = square_out_datapoints(new_house, gymminlat, gymmaxlat, gymminlong, gymmaxlong)

# albertmaxlat, albertminlong = ary(ary([51.672997, -1.293183])*1E7, dtype=int)
# albertminlat, albertmaxlong = ary(ary([51.671585, -1.291115])*1E7, dtype=int)

previous_time = get_time(gym[0])
start_time = get_time(gym[0])

gymming = []
for d in gym:
    new_time = get_time(d)
    if (new_time - previous_time).total_seconds() > phone_off_threshold:
        gymming.append([start_time, previous_time - start_time])
        start_time = new_time
    previous_time = new_time

gymming = ary(gymming)

with open("gymtime.csv","w") as f:
    for i in gymming:
        date = i[0].strftime("%D")
        duration = i[1].total_seconds()
        mins = str( int(duration//60) )
        tot_sec= str( duration )
        
        f.write(date+",")
        f.write(mins+",")
        f.write(tot_sec+"\n")
        
        print(i[0].ctime()[:-4], mins, tot_sec) #don't print the year