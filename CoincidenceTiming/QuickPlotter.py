#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = ["/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-16/Ascii/133Ba_spectrum.Spe",
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-16/Ascii/BG-subtracted-133Ba_spectrum.Spe",
			]
			#I've checked 22Na, 241Am, 44Ti. They all don't need background subtraction.
n=0
names = iter(['raw data','background subtracted'])
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ]
	data = data[:]
	plt.semilogy(data,label= str(n))
	#plt.semilogy(data,label=next(names))
plt.title("Spectrum of "+r"${}^{133}$Ba"+" ?")
plt.xlabel('channel')
plt.ylabel("counts")
plt.legend()
plt.show()
#plt.savefig("QuicklyPlotted.png")