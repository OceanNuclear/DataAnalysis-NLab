#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = [
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/TAC-Spectra/44Ti_Deconvolute_Coincidence_Decay_Period.Spe",
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/TAC-Spectra/Na-22-COIN-(FWHM-investigation)-SameSettingAsLastWeek.Spe",
			]
n=0
names = iter(['log scale','linear scale'])
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ] #cut the file at appropriate points
	data = data[:]
	# plt.plot(data,label= str(n))
	plt.semilogy(data,label= str(n))
plt.xlabel('channel')
plt.ylabel("counts")

plt.title("TAC spectrum of "+r"${}^{44}$Ti,"+"\n"+r"showing delay between $\gamma_{(0^-\rightarrow 1^-)}$ and $\gamma_{(1^-\rightarrow2^+)}$")
# plt.legend()
# plt.show()
plt.savefig("Deconvable_log.png")
# for n in range(len(data)):
# 	print(n, data[n])