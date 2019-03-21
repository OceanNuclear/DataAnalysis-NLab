#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
import pandas as pd
from scipy.optimize import curve_fit
#create subprogram to repetitively find out the mean and sigma of intensity at each thickness
def openFile(fileName):
	df = pd.read_csv(fileName, delimiter = "\t", header =1)
	thickness = []	#list of thickness of Fe plates used
	I = []	#list of mean intensities
	dI= []	#uncertainty on the mean

	for n in df:
		if float(n) != 9.3:
			#print("With thickness = ",n,"\n trial results are as follows \n ",df[n])
			thickness.append(float(n))
			I.append( np.mean(df[n]))
			dI.append(np.std( df[n], ddof=1)/sqrt(len(df[n]))) 
			#Applying Bessel's correction to obtain the population standard deviation;
			#because it is literally a blackbox and error propagation is impossible;
			#And divide by sqrt numData to get error on the mean
	thickness = ary(thickness)
	I = ary(I)
	dI = ary(dI)
	return thickness,I,dI, fileName[11:-4]

def fittedExp(x,A,B):
	return A*np.exp(-x/B)
fig, (ax1, ax2) = plt.subplots(2, sharex=True, gridspec_kw = {"height_ratios":[3,1]})

thickness_col, I_col, dI_col, col = openFile("Col.tsv")
ax1.errorbar(thickness_col,  I_col,  dI_col,   label=col  )
thickness_uncol, I_uncol, dI_uncol, uncol= openFile("Uncol.tsv")
ax1.errorbar(thickness_uncol,I_uncol,dI_uncol, label=uncol)

#Function fitting bit
[(a,b),cov] = curve_fit(fittedExp, thickness_col,I_col,sigma=dI_col,absolute_sigma=True, check_finite=True)#
da,db = np.sqrt(np.diag(cov))

residual = I_col - fittedExp(thickness_col,a,b)
xSmooth = np.linspace(np.min(thickness_col), np.max(thickness_col), 1000)
yCalcSmooth = fittedExp(xSmooth, a, b)
chiSq = sum( (residual/dI_col)**2 )
chiSqPerDoF = r"$\frac{\chi^2}{DoF} = $"+str( '{:0=3.2f}'.format( chiSq/(len(thickness_col)-2) ))
#End of function fitting bit
aString="A="+"{:0=2.2f}".format(a)
bString="B="+"{:0=2.2f}".format(b)
daString= r"$\sigma_A$="+'{:0=2.2f}'.format(da)
dbString= r"$\sigma_B$="+'{:0=2.2f}'.format(db)
fitEquation="fit = A*exp(-x/B)"+"where\n "+aString+","+bString+",\n"+daString+","+dbString
ax1.plot(xSmooth,yCalcSmooth,label=fitEquation, color = "r")#

#print(aString,"\n",bString)
ax1.set_ylim(ymin=0)
ax1.legend()
#ax1.annotate(fitEquation,[0,0.1])
ax2.errorbar(thickness_col,residual, yerr=dI_col, label=chiSqPerDoF)
ax2.plot(thickness_col, np.zeros(np.shape(thickness_col)), color="black")
ax2.legend()
ax2.set_title("residuals")

ax1.set_title("Dose measured by Ionization Chamber")
ax1.set_ylabel("Dose (μSv)")
ax2.set_ylabel("μSv")
ax2.set_xlabel("thickness of attenuating plates(mm)")

#plt.savefig("fitting.png",bbox_inches="tight")
plt.show()