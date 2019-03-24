#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

fname="CloseCounts.txt"
# fname="FarCounts.txt"

f=open(fname,"r")
data=f.readlines()
f.close()

x,y,z=[],[],[]
for line in data:
	line=line.split("\t")
	x.append(line[0])
	y.append(line[1])
	if len(line)>2:
		z.append(line[2])
x,y,z=ary([x,y,z],dtype=int)
plt.plot(x,y/z,marker="x")
plt.title("Angular variation of count rate at 2.95cm away from the source")
#plt.title("Angular variation of count rate at 10cm away from the source")
plt.xlabel("Angle")
plt.ylabel("Count rate (per second)")
plt.show()