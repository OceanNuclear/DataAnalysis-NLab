#!/home/ocean/anaconda3/bin/python3
from numpy import cos,log10, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sns
from fluxDists import *
#line 62 really confuses me.

#if __name__!="__main__":print(OneGrp_Thm)
def handleFittingResult(func,xdata,ydata,yerr,guess):
	absSigma=False
	assert xdata.ndim==2
	x,z = xdata.T
	numParam = len(guess)
	if numParam!=0:
		if len(np.unique(z))==1:
			func, guess = Swap2Single(func,"z",guess)
		elif len(np.unique(x))==1:
			func, guess = Swap2Single(func,"x",guess)
		popt, pcov = curve_fit(func, xdata, ydata, sigma=yerr, p0=guess,absolute_sigma=absSigma, check_finite=True)
		σ2 = np.diag(pcov)
	else:
		popt = []
	residual = ydata - variablePFunction(func,xdata,popt)
	chiSq = sum( (residual/yerr)**2 )
	chiSqPerDoF = s( chiSq/(len(xdata)-numParam) )
	if not absSigma:	yerr=yerr*sqrt(chiSq/(len(xdata)-numParam)); chiSqPerDoF="1.00"
	if numParam>1:
		cov = offdiag(pcov)
		print("covariances=",cov)
		#print warning when covariance reaches a certain limit:
		[print("warning: covariance is a bit pathological!!!!!!!!!!!!!!!!!!!!!!!") for n in cov if abs(n)>900]
	equation = ""
	for n in range(len(popt)):
		equation += chr(97+n)+"=" + s(popt[n])#optimum value
		equation += r'$\pm$'      + s(sqrt(σ2)[n])#error
		equation += "\n"#new line
	equation += (r'$\frac{\chi^2}{DoF}$' +"=" +chiSqPerDoF)
	print(equation)
	xy_residual = append_axis(xdata,residual)
	xy_residual = append_axis(xy_residual,yerr)
	xy_residual = pd.DataFrame(xy_residual,columns=["x","z","diff","errbar"])
	if xy_residual.nunique()["z"]!=1 and xy_residual.nunique()["x"]!=1:
		#first make a residual plot
		plotObject = facetGrid(xy_residual,equation)
	else:
		if xy_residual.nunique()["z"]==1:
		#create residual plot
			x_residual_err = pd.DataFrame(xy_residual,columns=["x","diff","errbar"])
			#plotObject = residPlot(x_residual_err,equation)
			plotObject = (x_residual_err,equation)#for the moment I'm returning the DataFrame as the plotObject
		elif xy_residual.nunique()["x"]==1:
			z_residual_err = pd.DataFrame(xy_residual,columns=["z","diff","errorbar"])
			plotObject = (z_residual_err,equation)
	#And then create mesh
	res = 400
	x0,x1,z0,z1 = min(x),max(x),min(z),max(z)
	[Δx, Δz]=[(x1-x0),(z1-z0)]
	if Δx!=0:
		x = np.linspace(x0,x1,res)
	else:#for a single slice of constant x???
		assert xy_residual.nunique()["x"]==1
		x = ary(x[0])
		Δx = Δz	#such that the resolution will be the same as this.
	zres= int(res*Δz/Δx)
	z = np.linspace(z0,z1,zres+1)
	mesh = mymesh(x,z) #gives shape==(len(x),2)
	yCalcSmooth = variablePFunction(func,mesh,popt)
	smoothData = append_axis(mesh, yCalcSmooth)
	return smoothData, plotObject

def Swap2Single(func,x_z,guess):
	#oh boy this looks like a shit ton of mess I apologize I was programming within a time constraint, clarity was not my highest priority.
	assert x_z=="x" or x_z=="z"
	if x_z=="x":#constant x, removing ability to fit on alpha.
		#only variation in z
		if func==FastSquare:
			return FastSquarex, guess[:-1] #only care about tau
		if func==FastSquare_τ:
			#raise ValueError#only degree of freedom(tau) already removed, therefore not allowed.
			return FastSquare_τ, guess[:]
		if func==FastSph:
			return FastSph, guess[:]#still have to keep that 1DoF
		if func==OneGrp_Thm:
			return OneGrp_Thmx, guess[:-1] #only care about L
		if func==TwoGrp_Thm:
			return TwoGrp_Thmx, guess[:-1] #only care about L
		if func==TwoGrp_redefine_τ:
			return TwoGrp_redefine_τx, guess[:-1] #only care about L, with possibility of redefining tau
		if func==OneGrp_Thm_Sph:
			return OneGrp_Thm_Sph, guess[:]
		if func==OneGrp_Thm_Sph:
			return OneGrp_Thm_Sph, guess[:]
		if func==ThirdOrd_OneGrp_Thmz:
			return ThirdOrd_OneGrp_Thmz,guess[:]
		if func==ThirdOrd_TwoGrp_Thmz:
			return ThirdOrd_TwoGrp_Thmz,guess[:]
		if func==OneGrp_ThmNoBD:
			return OneGrp_ThmNoBDx, guess[-1:]#only cosines matters
	else:#only variation in x
		if func==FastSquare:
			return FastSquare_τ, guess[-1:]	#keeps tau constant wrt. variation in x, only care about alpha
		if func==FastSquare_τ:
			return FastSquare_τ, guess[:]	#don't care about variation in tau, which is kept constant here anyways.
		if func==FastSph:
			return FastSph, guess[:]#still only 1DoF
		if func==OneGrp_Thm:
			return OneGrp_Thmz, guess[-1:]	#keeps z constant, #don't care about variation in L
		if func==TwoGrp_Thm:
			return TwoGrp_Thmz, guess[-1:]	#don't care about variation in L
		if func==TwoGrp_redefine_τ:	
			return TwoGrp_redefine_τz,guess[-1:]	#don't care about variation in L
		if func==OneGrp_Thm_Sph:
			return OneGrp_Thm_Sph, guess[:]
		if func==ThirdOrd_OneGrp_Thmz:
			return ThirdOrd_OneGrp_Thmz,guess[:]
		if func==ThirdOrd_TwoGrp_Thmz:
			return ThirdOrd_TwoGrp_Thmz,guess[:]
		if func==FixL:
			return FixL, guess[:]
		if func==FixLtau:
			return FixLtau, guess[:]
		if func==OneGrp_ThmNoBD:
			return OneGrp_ThmNoBDz, guess[:-1]