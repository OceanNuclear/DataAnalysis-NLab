#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
fileName = [
"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Xrays/Spr9_Attenuation/AnnularAm241Source/Fe_Attenuator_Brass.Spe",
"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Xrays/Spr9_Attenuation/AnnularAm241Source/Ni_Attenuator_Brass.Spe",
"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Xrays/Spr9_Attenuation/AnnularAm241Source/Cu_Attenuator_Brass.Spe",
"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Xrays/Spr9_Attenuation/AnnularAm241Source/Zr_Attenuator_Brass.Spe",
"/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Xrays/Spr9_Attenuation/AnnularAm241Source/No_Attenuator_Brass.Spe",
			]
			#I've checked 22Na, 241Am, 44Ti. They all don't need background subtraction.
n=0
names = iter(['Fe','Ni',"Cu","Zr","unattenuated, scaled down by a factor of 10"])
datalist=[]
for fn in fileName:
	n+=1
	f = open(fn,"r")
	data = f.readlines()
	f.close()
	data = [ int(x) for x in data[12:2060] ] #cut the file at appropriate points
	data = ary(data[0:600])
	if n==5:
		data=data/9
	datalist.append(data)
	plt.plot(data,label= next(names),alpha=0.8)
datalist=ary(datalist)
plt.xlabel('channel')
plt.ylabel("counts")
def annot(channel,text):
	x=int(channel)
	y = min(datalist[:,x])
	print(datalist[:,x])
	Δy=+50
	alength=30
	plt.arrow(x,(y-Δy-alength),0,Δy,head_length=alength,head_width=15,zorder=10)
	plt.annotate(text,[x,y-Δy-alength],ha="center",va="top")
	return
annot(231.6034856,"Fe K-edge")
# annot(229.8787172,"Fe K-alpha")
annot(271.5335012,"Ni K-edge")
# annot(269.1904196,"Ni k-alpha")
annot(292.8164924,"Cu K-edge")
annot(585.8318636,"Zr K-edge")
annot(82.65509,"Zr L-edge")
if "22Na"!="22Na":
	plt.title("Spectrum of"+r"${}^{22}$Na"+" with the proper gate applied to select the 511 keV peak")
	start,end=ary([[600,550],[1000,200]])
	Δx,Δy=end-start
	plt.arrow(start[0],start[1],Δx,Δy,head_length=30,head_width=30)
	text_bl_coord=np.mean([start,end],axis=0)
	plt.annotate("511keV peak shifted\nafter scaling up the gain",text_bl_coord)
# plt.title("TAC spectrum of "+r"${}^{44}$Ti,"+"\n"+r"showing delay between $\gamma_{(0^-\rightarrow 1^-)}$ and $\gamma_{(1^-\rightarrow2^+)}$")
plt.legend()
plt.title("Spectra of Brass fluorescence X ray after being attenuated by various elements")
plt.show()
# plt.savefig("Deconvable.png")