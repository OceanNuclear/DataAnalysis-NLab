#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = [#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/Calibrations/11-16/133Ba_spectrum.Spe",
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/Ascii/133Ba_spectrum.Spe",
			#'/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/Calibrations/11-16/241Am_spectrum.Spe',
			#'Calibrations/12-07/68Ge_Det_B_44Ti_67_78_peaks_calibraton.Spe',
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/Calibrations/11-16/241Am_spectrum.Spe",
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/Ascii/241Am_spectrum.Spe",
			#
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/44Ti_Deconvolute_Coincidence_Decay_Period.Spe",
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/ShowEnergySelection-cutoff/Det_A_44Ti_67_SCA_Window.Spe",
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/ShowEnergySelection-cutoff/Det_B_44Ti_67_78_SCA_Window.Spe",
			#"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Na-22-COIN-(FWHM-investigation)-SameSettingAsLastWeek.Spe",
			]
n=0
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ]
	plt.semilogy(data,label=str(n))
plt.legend()
plt.show()