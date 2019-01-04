#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = [#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/FromJack/Labs_Annihilation/Calibrations/11-16/133Ba_spectrum.Spe",
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/FromJack/Labs_Annihilation/Ascii/133Ba_spectrum.Spe",
			#'/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/FromJack/Labs_Annihilation/Calibrations/11-16/241Am_spectrum.Spe',
			#'FromJack/Labs_Annihilation/Calibrations/12-07/68Ge_Det_B_44Ti_67_78_peaks_calibraton.Spe',
			'FromJack/Labs_Annihilation/68Ge_Det_B_44Ti_67_78_peaks_calibraton.Spe',
			#'FromJack/Labs_Annihilation/Det_A_44Ti_67_78_peaks_calibraton.Spe',
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/FromJack/Labs_Annihilation/Calibrations/11-16/241Am_spectrum.Spe",
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/FromJack/Labs_Annihilation/Ascii/241Am_spectrum.Spe",
			]
n=0
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:300] ]
	plt.semilogy(data,label=str(n))
plt.legend()
plt.show()