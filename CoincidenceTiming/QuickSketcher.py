#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = [
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/Det_B_44Ti_67_78_peaks_calibraton.Spe",
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/ShowEnergySelection-cutoff/Det_B_44Ti_67_78_SCA_Window.Spe",
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/Det_A_44Ti_67_78_peaks_calibraton.Spe",
			"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/Calibration/ShowEnergySelection-cutoff/Det_A_44Ti_67_SCA_Window.Spe",
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-23/Calibration/22Na_B.Spe",
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-30/22Na-B-511Window-Bipolar-0.5shaping.Spe",
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/TAC-Spectra/44Ti_Deconvolute_Coincidence_Decay_Period.Spe",
			# "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/12-07/TAC-Spectra/Na-22-COIN-(FWHM-investigation)-SameSettingAsLastWeek.Spe",
			]
			#I've checked 22Na, 241Am, 44Ti. They all don't need background subtraction.
n=0
names = iter(['Detector B before gate application ','Detector B after gate application',"Detector A before gate application","Detector A after gate application","5"])
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ] #cut the file at appropriate points
	if n==2:
		data = ary(data[:])/6
	if n==4:
		data = ary(data[:])*2.7
	plt.semilogy(data,label= next(names),alpha=0.8)
	# plt.semilogy(data,label=next(names), alpha=0.4)
plt.xlabel('channel')
plt.ylabel("counts")
if "22Na"!="22Na":
	plt.title("Spectrum of"+r"${}^{22}$Na"+" with the proper gate applied to select the 511 keV peak")
	start,end=ary([[600,550],[1000,200]])
	Δx,Δy=end-start
	plt.arrow(start[0],start[1],Δx,Δy,head_length=30,head_width=30)
	text_bl_coord=np.mean([start,end],axis=0)
	plt.annotate("511keV peak shifted\nafter scaling up the gain",text_bl_coord)
# plt.title("TAC spectrum of "+r"${}^{44}$Ti,"+"\n"+r"showing delay between $\gamma_{(0^-\rightarrow 1^-)}$ and $\gamma_{(1^-\rightarrow2^+)}$")
plt.legend()
plt.title("Plot showing the spectra before and after applying energy selection gates")
plt.show()
# plt.savefig("Deconvable.png")