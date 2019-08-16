#!/home/ocean/anaconda3/bin/python3
import json
from urllib import request as rq
import sys
import time

with rq.urlopen('https://wakatime.com/share/@6461bdda-9d02-4ac3-a62b-a6cccb1fc7c9/68792e86-ecb8-46ac-be31-9166aaeda0bf.json') as url:
    data = json.loads(url.read().decode())["data"]

def savejson():
    file = json.dumps({"data": data})
    date = time.strftime("%Y-%m-%d")
    with open(date+".json", "w") as f:
        f.save(file)
    return
    
def savecsv():
    date = time.strftime("%Y-%m-%d")
    with open(date+".csv","w") as f:
        for i in data:
            date = i["range"]["date"]
            dig_time = i["grand_total"]["digital"]
            total_sec = i["grand_total"]["total_seconds"]
            f.write(date)
            f.write(",")
            f.write(str(dig_time))
            f.write(",")
            f.write(str(total_sec))
            f.write("\n")

if __name__=="__main__":
    try:
        arg = sys.argv[1]
    except IndexError:
        pass
    if arg =="json":
        savejson()
    if arg=="csv":
        savecsv()
    for i in data:
        date = i["range"]["date"]
        total = i["grand_total"]["digital"]
        print(date, total)
