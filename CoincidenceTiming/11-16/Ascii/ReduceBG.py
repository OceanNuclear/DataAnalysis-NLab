#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

#get filename
filename = input("file name without .Spe?")
SPE= ".Spe"

#read data file
f = open(filename+SPE,'r')
data = f.readlines()
f.close()
#read background and convert to array.
b = open('Background.Spe','r')
BG = b.readlines()
b.close()
BG = ary(BG[12:2060],dtype=float)

if __name__=="__main__":
	#manipulating the text
	prepend= data[:12]
	append = data[2060:]
	#minus bg
	data = ary(data[12:2060],dtype=float) - BG/1120* int(prepend[9].split()[0])
	#data = np.clip(data,0,None)
	data = ary(np.round(data),dtype=int)
	
	f = open("BG-subtracted-"+filename+SPE,"w")
	for line in prepend:
		f.write(line)
	for line in data:
		f.write('{:8d}'.format(line)+'\n')
	for line in append:
		f.write(line)
	f.close()