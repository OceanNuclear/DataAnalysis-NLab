#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
def get_data(fileName):
	f = open(fileName,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:8204] ]
	return ary(data)

prepending = "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Attenuation/FromJack/NaIDetector/Spectra/Fe/Uncollimated/Co60_"
appending = "_plate.Spe"
for n in range (0,5):
	fileName = prepending+str(n)+appending
	data =get_data(fileName)
	if n==0:
		data= data/5
	plt.semilogy(data,alpha=0.7)
plt.show()