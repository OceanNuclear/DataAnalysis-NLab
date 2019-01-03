#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
prepending = "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/FromJack/Labs_Annihilation/Ascii/Operating Voltage and Gain/"
appending  = "_50_Co60.Spe"
for name in ['600V','650V','800V']:
	#vol = str(500+num*50)+"V"
	fileName = prepending+name+appending
	f = open(fileName,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ]
	data = 100000*ary(data)/sum(data)#cheeky normalization
	plt.semilogy(data, label=r"$V_{app}$="+name, alpha=0.8)
plt.legend()
plt.xlabel("channel number")
plt.ylabel("counts per channel")
#plt.text(1,1,"Area under each curve = total number of counts is approximately constant")
plt.suptitle("Effect of increasing the applied voltage on the PMT")
plt.title("Amplifier coarse gain = 50, fine gain=0, source used = "+r"${}^{60}$Co")
#plt.savefig("IncreaseVapp.png")
plt.show()