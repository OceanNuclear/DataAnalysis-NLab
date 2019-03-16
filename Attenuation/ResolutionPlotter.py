#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

f = open("Resolution.txt")

data = f.readlines()
FW=[]
def calibrated(channel):
	#Look here!
	#Awaiting calibration equation (parameters)
	energy=channel
	return energy
ax=plt.subplot()
for line in data:
	if not line.startswith("#"):
		E.append(  line.split("\t")[0])
		FW.append( line.split("\t")[1])
		err.append(line.split("\t")[2])
	else:
		if len(FW)!=0:
			E,FW,err=ary(E,dtype=float),ary(FW,dtype=float),ary(err,dtype=float)
			plt.errorbar(E,calibrated(FW)/E,calibrated(err)/E,label=t,  linestyle='',marker="x",markersize=4,capsize=3)
		t=line[1:-1]
		E, FW, err = [], [], []
plt.legend()
plt.show()