#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
import sys
sys.path.append("..")
from HiddenSubprograms import *

global target_y
target_y=-71

#x,z, AllFlux, allFErr = choose_y("../n-Diff-new.csv",y_val=target_y)
x2,z2,FastFlux,fastFErr=choose_y("../CadmiumNew.csv",y_val=target_y)
print("for y=",target_y)
for xelem in x2[:7]:
	zchosen=[]
	flux=[]
	for n in range(len(z2)):#run through the whole dataset
		if x2[n]==xelem:	#to find the data with matching x
			#print(x2[n],"\t ",z2[n]," \t",FastFlux[n])
			zchosen.append(z2[n])
			flux.append(FastFlux[n])
	plt.plot(zchosen[:  ],     flux ,label="x="+str(xelem)+" cm")
plt.title("Fast neutron flux variation with height at different x, y="+str(target_y))
plt.xlabel("z coordinate (cm)")
plt.legend()
plt.savefig(str(target_y)+".png")
#plt.show()