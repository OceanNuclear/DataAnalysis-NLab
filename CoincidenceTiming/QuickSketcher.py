#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = [
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/Det_A_44Ti_67_78_peaks_calibraton.Spe",
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/ShowEnergySelection-cutoff/Det_A_44Ti_67_SCA_Window.Spe",
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/Det_B_44Ti_67_78_peaks_calibraton.Spe",
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/ShowEnergySelection-cutoff/Det_B_44Ti_67_78_SCA_Window.Spe",
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-30/22Na-B-511Window-Bipolar-0.5shaping.Spe",
			]
			#I've checked 22Na, 241Am, 44Ti. They all don't need background subtraction.
n=0
names = iter(['before','after',"3","4"])
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ] #cut the file at appropriate points
	data = data[:]
	# plt.semilogy(data,)#label= str(n))
	plt.semilogy(data,label=next(names))
plt.title("Gate applied onto a spectra of"+r"${}^{22}$Na"+"")
plt.xlabel('channel')
plt.ylabel("counts")
plt.legend()
plt.show()
#plt.savefig("QuicklyPlotted.png")