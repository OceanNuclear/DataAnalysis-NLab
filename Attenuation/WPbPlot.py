#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
prepending	= "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Attenuation/FromJack/NaIDetector/Spectra/"
#material	= "Pb/Collimated/Co60_"
material	= "W/Uncollimated/W_"
#appending	= "BIG_Pb.Spe"
appending	= "_Plate.Spe"
for num in range(1,6):
	fileName = prepending+material+str(num)+appending
	f = open(fileName,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:8204] ]
	plt.semilogy(data,alpha=0.5,label=str(num)+" plate, "+"W")
plt.legend()
plt.show()