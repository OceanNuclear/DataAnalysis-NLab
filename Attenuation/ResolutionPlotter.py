#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

f = open("Resolution.txt")
logscale= True

data = f.readlines()
FW=[]
def calibrated(channel):
	#Look here!
	#Awaiting calibration equation (parameters)
	energy=channel
	return energy
ax=plt.subplot()
for line in data:
	if not (line.startswith("#") or len(line)<=3):
		E.append(  line.split("\t")[0])
		FW.append( line.split("\t")[1])
		err.append(line.split("\t")[2])
	else:
		if len(FW)!=0:
			E,FW,err=ary(E,dtype=float),ary(FW,dtype=float),ary(err,dtype=float)
			R=calibrated(FW)/E
			dR=calibrated(err)/E
			if logscale:
				plt.errorbar(E,R,dR/R,label=t,  linestyle='',marker="x",markersize=4,capsize=3)
			else:
				plt.errorbar(E,R,dR,label=t,  linestyle='',marker="x",markersize=4,capsize=3)
		t=line[1:-1]
		E, FW, err = [], [], []
ax.set_xlabel("E (keV)")
ax.set_ylabel("R(E)")
ax.legend()
if logscale:
	ax.set_xscale("log", nonposx='clip')
	ax.set_yscale("log", nonposy='clip')
	plt.savefig("loglogscaleResolution.png",bbox_inches="tight")
#plt.show()