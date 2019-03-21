#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
import glob
from scipy import signal as sig
p1,p0= [5.0256848,  83.10133259]
directory="OverlayPlots/Convoluted/"
def thickness(inp):
	sources = {
	1: ["./FromJack/NaIDetector/Spectra/Fe/*ollimated/Co60_1_plate.Spe", 6.3 ,0.05],
	2: ["./FromJack/NaIDetector/Spectra/Fe/*ollimated/Co60_2_plate.Spe",12.65,0.05*sqrt(2)],
	3: ["./FromJack/NaIDetector/Spectra/Fe/*ollimated/Co60_3_plate.Spe",19.07,0.05*sqrt(3)],
	4: ["./FromJack/NaIDetector/Spectra/Fe/*ollimated/Co60_4_plate.Spe",25.56,0.1],
	}
	print(sources.get(inp))
	path, t, dt = sources.get(inp)
	path=glob.glob(path)
	path.sort()
	return [path,t,dt]
def Col_info(inp):
	sources= {
	"uncol":["./FromJack/NaIDetector/Spectra/Fe/Uncollimated/Co60_*_plate.Spe","Uncollimated"],
	"Uncol":["./FromJack/NaIDetector/Spectra/Fe/Uncollimated/Co60_*_plate.Spe","Uncollimated"],
	"col" : ["./FromJack/NaIDetector/Spectra/Fe/Collimated/Co60_*_plate.Spe","Collimated"],
	"Col" : ["./FromJack/NaIDetector/Spectra/Fe/Collimated/Co60_*_plate.Spe","Collimated"],
	"Wuncol":["./FromJack/NaIDetector/Spectra/W/Uncollimated/W_*_Plate.Spe","Collimated"],
	}
	path, collimation = sources.get(inp)
	path=glob.glob(path)
	path.sort()
	if "_0_" in path[0]:
		path=path[1:]+[path[0]]
	return [path,collimation]

def normalizeProb(ar):
	return ary(ar)/np.sum(ar)

def SlidingAvg(data):
	winsize=11#must be an odd number
	spread=3
	win = sig.gaussian(winsize,spread)
	win = normalizeProb(win)
	excess=int((winsize-1)/2)
	return np.convolve(win,data)[excess:-excess]

# filenames, t,dt = thickness(1);T=True
filenames, collimation=Col_info("col");T=False
if T:
	for i in range(len(filenames)):
		f=open(filenames[i],"r")
		print("opening file ",filenames[i])
		lines=f.readlines()
		f.close()
		data = [ int(x) for x in lines[12:8204] ]
		xaxis=(ary([i+1 for i in range(len(data))]) - p0)/p1
		collimationness=filenames[i].split("/")[5]
		plt.semilogy(xaxis,SlidingAvg(data),alpha=0.4,label=collimationness)
	plt.title("thickness="+str(t)+"±"+str(dt)+" mm")
	plt.xlabel("Energy (keV)")
	plt.ylabel("Counts per minute live time")
	plt.legend()
	plt.savefig(directory+str(t)+"mm_Fe.png")
elif not T:
	thicknesses=[ 6.3 ,12.65,19.07,25.56]
	thicknesses=[str(i) for i in thicknesses]
	thicknesses+=["0"]
	dts = ["{:.3f}".format(0.05*sqrt(i)) for i in range (1,5)]
	dts += ["0"]
	material,collimation=filenames[0].split("/")[4:6]
	if material=="W":
		thicknesses=[3.23, 6.63, 9.93, 13.28, 16.54, 0]
		dts=[0.05, 0.07071067811865477, 0.08660254037844388, 0.1, 0.1118033988749895, 0]
		thicknesses=[str(x) for x in thicknesses]
		dts=[str(x) for x in dts]
	for i in range (len(filenames)):
		f=open(filenames[i],"r")
		print("opening file ", filenames[i])
		lines=f.readlines()
		f.close()
		data = [ int(x) for x in lines[12:8204] ]
		if dts[i]=="0" or material=="Pb":
			data=[x/5 for x in data]
		xaxis=(ary([i+1 for i in range(len(data))]) - p0)/p1
		plt.semilogy(xaxis,SlidingAvg(data),alpha=0.3,label=thicknesses[i]+"±"+str(dts[i])+" mm")
		#plt.plot(xaxis,data,alpha=0.3,label=thicknesses[i]+"±"+str(dts[i]))
	titletext=collimation+" geometry attenuated by "+material+" plates of various thicknesses"
	plt.xlabel("Energy (keV)")
	plt.ylabel("Counts per minute live time")
	plt.title(titletext)
	plt.legend()
	plt.savefig(directory+collimation+material+".png")