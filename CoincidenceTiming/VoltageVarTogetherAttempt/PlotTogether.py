#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

'''
covariances= [-7.033937448658753e-25]
r"$a=1.29e-19 \pm 5.91e-43$"+"\n"+r"$b=7.81 \pm 8.38e-7$"
r"$\frac{chi^2}{DoF}=1.03 \times 10^3$"
cov(a,b)=$-7.03 \times 10^{-25}$
covariances= [-5.074285685368331e-25]
r"$a=1.42 \times 10^{-19} \pm 4.71 \times 10^{-43}$"+"\n"+r"$b=7.81\pm .47 \times 10^{-7}$"
r"$\frac{chi^2}{DoF}$ =1.26 \times 10^3"
cov(a,b)=$-5.07 \times 10^{-25}$

'''
Vmin=500
Vmax=800
def FitPowerCurve(a,b):
	x=np.linspace(Vmin,Vmax)
	LineWithAB=a*x**b
	return [x,LineWithAB]
def fit(x,a,b):
	return a*x**b
def SwapOrder(FourElemAry):
	return FourElemAry[3],FourElemAry[1],FourElemAry[2],FourElemAry[0]
if __name__=="__main__":
	fnameList=["Centroids.txt","Centroids2.txt"]
	
	peakname=iter(["1.1MeV peak","1.3MeV peak"])
	residpeaknames=iter(
	[r"$\frac{\chi^2}{DoF} =1.26 \times 10^3$",
	r"$\frac{\chi^2}{DoF} =1.03 \times 10^3$"])
	
	fitnames=iter([
	r"$a=1.29 \times 10^{-19} \pm 5.91 \times 10^{-43}$"
	+"\n"+r"$b=7.81 \pm 8.38 \times 10^{-7}$"
	+"\n"+r"cov($a,b$)=$-5.07 \times 10^{-25}$",
	r"$a=1.42 \times 10^{-19} \pm 4.71 \times 10^{-43}$"
	+"\n"+r"$b=7.81\pm .47 \times 10^{-7}$"
	+"\n"+r"cov($a,b$)=$-5.07 \times 10^{-25}$"])

	ab=iter([[1.2924485918824035e-19,7.806785793269601],[1.423837789836701e-19,7.811060744101789]])
	
	dummy, (ax1, ax2) = plt.subplots(2, sharex=True,gridspec_kw={'height_ratios':[3,2]})
	
	for fname in fnameList:
		f=open(fname,"r")
		data=f.readlines()
		f.close()
		x,y,dy=[],[],[]
		for line in data:
			line=line.split("\t")
			x.append(line[0])
			y.append(line[1])
			dy.append(line[2])
		x,y,dy=ary([x,y,dy],dtype=float)
		a,b=next(ab)
		resid=y-fit(x,a,b)
		ax1.errorbar(x,y,yerr=dy,fmt ='x',capsize=5,label=next(peakname),)
		ax2.errorbar(x,resid,yerr=dy,fmt="x",capsize=5,label=next(residpeaknames),)
		xsm,ysm=FitPowerCurve(a,b)
		ax1.plot(xsm,ysm,label=next(fitnames),)
	ax1.set_ylabel("Centroid channel")
	ax2.set_xlabel("applied voltage on the detector's PMT (V)")
	ax1.set_title("Variation of pulse height of the two "+r"${}^{60}Co$"+" peaks"+"\n fitted to a function of "+r"$y=ax^b$")
	handles, labels = ax1.get_legend_handles_labels()
	SwapOrder(handles)
	ax1.legend(SwapOrder(handles), SwapOrder(labels))
	ax2.axhline(color="black")
	ax2.set_title("residuals")
	ax2.legend()
	plt.show()
	# plt.savefig("FinalMergedVoltVarFit.png",dpi=100,size_inches=[10,15])