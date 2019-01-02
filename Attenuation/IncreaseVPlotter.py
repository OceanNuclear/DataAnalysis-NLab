#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
prepending = "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Attenuation/FromJack/NaIDetector/ForCalibration/Co60_"
appending  = "0V.Spe"
for num in ["50","55","60","65","70","75","80"]:
	fileName = prepending+num+appending
	f = open(fileName,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:8204] ]
	plt.semilogy(data)
plt.show()