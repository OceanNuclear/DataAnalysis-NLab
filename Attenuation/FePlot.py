#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
prepending	= "/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/Attenuation/FromJack/NaIDetector/Spectra/"
material	= "Fe/Collimated/Co60_"
material	= "Fe/Uncollimated/Co60_"
appending	= "_plate.Spe"
for geom in ["Col","Uncol"]:
	material=material[-15:]
	if geom=='Col':
		material = "Fe/C"+material
	elif geom=="Uncol":
		material="Fe/Unc"+material
	for num in range(1,5):
		fileName = prepending+material+str(num)+appending
		f = open(fileName,"r")
		data = f.readlines()
		f.close()
		data = [ int(x) for x in data[12:8204] ]
		#gotta wait for the calibration equation to come in to plot the x axis properly.
		plt.semilogy(data,alpha=0.55-num*0.1,label=str(num)+" plate, "+geom)
plt.xlabel("energy (keV)")
plt.legend()
plt.show()