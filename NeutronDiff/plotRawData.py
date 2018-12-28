#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns
#fluxFit.py only deals with reading data and then fitting them.
from HiddenSubprograms import *	#other lower level programs
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
global FastFlux
global ThmFlux
global τ
τ = 368	#unit:cm^2
#<Change these>
target_y=-71	#picking the xz plane that contains the source.
fast = True
norm = False
#</Change these>
'''____And then the rest of it is just boring computation____'''
Thm = not fast
fileName=""
x,z, AllFlux, allFErr = readData("n-Diff-new.csv",y_val=target_y)
x2,z2,FastFlux,fastFErr=readData("CadmiumNew.csv",y_val=target_y)
xzfast = ary([x2,z2]).T#of shape (49,2)
xzThm,ThmFlux,ThmErr = Extended_thermal_flux(x,z,AllFlux,allFErr,x2,z2,FastFlux,fastFErr)
minf, maxf= None, None
if norm:
	fileName+="normalized "
	maxf=48246.100000000006
	minf=0.05
if Thm:
	fileName+="Thermal"
elif fast:
	fileName+= "Fast"
fileName+=" Neutron flux count rate at y="+str(target_y)+" cm"
def abbreviateName(longname):
	assert type(longname)==str
	abbFilename = longname.replace(" Neutron flux count rate at ","")
	abbFilename = abbFilename.replace(" cm","")
	abbFilename = abbFilename.replace("y=","_")
	abbFilename = abbFilename.replace("alized ","")
	return abbFilename
abbFilename = abbreviateName(fileName)
if fast:
	cmap = sns.blend_palette(["g","y"],as_cmap=True)
else:
	#cmap = sns.blend_palette(["r","b"],as_cmap=True)
	cmap = sns.diverging_palette(250, 15, s=75, l=40, center="dark",as_cmap=True)
print("for y=",target_y,",  ", fileName,sep="")
if __name__=="__main__":
	if ("Fast" in fileName) or ("fast" in fileName):
		heatmapDF = ToDataFrame(xzfast,FastFlux,fastFErr)
	else:
		heatmapDF = ToDataFrame(xzThm, ThmFlux, ThmErr  )
	x,z,flux,err = heatmapDF.values.T #resuing the x,z variables for more important things
		#must provide guess value
	assert heatmapDF.nunique()["z"]>1
	ax = plt.subplot(111)
	heatmapDF = heatmapDF.pivot("z","x","flux")
	heat = sns.heatmap(heatmapDF,ax=ax,cmap = cmap,vmin=minf,vmax=maxf,cbar_kws={'label':'counts/s'})
	print(minf,maxf)
	heat.invert_yaxis()
	#plot the actual fit (in heat map form)
	#Two cmaps to choose from, both from seaborn:
	if "formatting"=="formatting":# can remove anytime if I don't like the formatting:
		ax.set_xlabel("x (cm)")
		ax.set_ylabel("z (cm)")
		ax.set_title(fileName)
		plt.tight_layout()
	plt.savefig("Printable/Raw/"+abbFilename+" HeatMap.png")