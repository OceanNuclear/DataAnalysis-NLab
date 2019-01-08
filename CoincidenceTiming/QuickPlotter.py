#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = ["/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-16/Calibration/22Na_spectrum.Spe",
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-16/Calibration/22Na_spectrum2.Spe",
			]
n=0
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ]
	data = data[:]
	plt.semilogy(data,label=str(n))
plt.legend()
plt.show()