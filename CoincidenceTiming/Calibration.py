#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
def Readxydy(fileName):
	f = open (fileName,'r')
	data = f.readlines()
	f.close()

	x,y,dy,labels=[],[],[],[]
	for line in data:
		if line.startswith("#"):
			prevLabel = line.replace("\n","").replace("#","")
		elif line!="\n":#if line is not empty
			line = line.split("\t")
			x.append (line[0])
			y.append (line[1])
			dy.append(line[2])
			labels.append(prevLabel)
	x = ary(x,dtype=float)
	y = ary(y,dtype=float)
	dy = ary(dy,dtype=float)
	return (x,y,dy,labels)
def Continuous(x):
	return np.linspace(min(x),max(x),100, endpoint=True)

(x,y,dy,labels)=Readxydy('Calib.txt')
global fit
fit = np.polyfit(x,y,1, w=(1/dy**2) )
fitFunc = np.poly1d(fit)

dummy, (ax1, ax2) = plt.subplots(2, sharex=True,gridspec_kw={'height_ratios':[3,2]})
for n in range(len(x)):
	ax1.errorbar(x[n],y[n],dy[n],fmt='.',label=labels[n])

if 'sophisticated'=='sophisticated':
	#Auxillary stuff around the plot
	ax1.set_title("With "+r"${}^{108} Ag^m$"+"data")
	ax1.set_ylabel("channel")
	ax2.set_xlabel("Energy(keV)")
	#plt smooth function
	xsm = Continuous(x)
	ysm = fitFunc(xsm)
	ax1.plot(xsm,ysm,label=str(fitFunc))
	ax1.legend()
if "residual"=="residual":
	resid = y-fitFunc(x)
	ax2.errorbar(x,resid,dy,fmt='.')
plt.show()

def inverseFunc(Y):
	m = fit[0]
	c = fit[1]
	X = (1/m)*Y - c/m
	return X
while True:
	In = input("Energy or Channel number?")
	if In=="E":
		E = float(input("Energy = "))
		print(fitFunc(E))
	if In=="C":
		C = float(input("Channel = "))
		print(inverseFunc(C))
	if In=='q' or In=='Q':
		break
'''
y = mx+c
(y-c)/m=x
x = (1/m)*y -c/m
'''