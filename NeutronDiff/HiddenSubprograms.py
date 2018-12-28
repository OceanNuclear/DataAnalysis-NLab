#!/home/ocean/anaconda3/bin/python3
from numpy import cos,log10, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
from scipy.optimize import curve_fit
import pandas as pd
import seaborn as sns
#print("HiddenSubprograms",__name__)
#The following list of subprogram is, with a few exceptions, alphabetically sorted.
def quadrature(xlist):
	assert xlist.ndim==1
	squares = [x**2 for x in xlist]
	return sqrt(np.sum(squares))
def add_y(xz,y_val):
	shape = np.shape(xz)
	assert len(shape)==2 and shape[1]==2
	[x,z] = xz.T
	y = np.zeros_like(x)*y_val
	xyz = ary([x,y,z]).T	#manipulating data such that it becomes the form we want
	return xyz
def append_axis(x,y):
	if np.ndim(x)==1:#assume 
		assert np.shape(x)==np.shape(y)
		xy = ary([x,y]).T
	if x.ndim==2:
		assert np.shape(x)[:1]==np.shape(y)
		xy = [axis for axis in ary(x).T]
		xy.append(ary(y))
		xy = ary(xy).T
	return xy
def clip_into_shape(x,z,AllFlux,AllErr,x2,z2,FastFlux,FastErr):
	ThmFlux = np.zeros_like(FastFlux)
	ThmErr  = np.zeros_like(FastErr)
	for n in range(len(FastFlux)):
		mask = (z==z2[n])*(x==x2[n])
		(ind,)= np.nonzero(mask)
		ind = ind[0]
		ThmFlux[n] = AllFlux[ind]-FastFlux[n]
		ThmErr[n] = quadrature(ary([AllErr[ind],FastErr[n]]))
	xz = append_axis(x2,z2)
	return xz,ThmFlux, ThmErr
def Extended_thermal_flux(x,z,AllFlux,AllErr,x2,z2,FastFlux,FastErr):
	ThmFlux = AllFlux - AllFlux
	ThmErr  = AllErr  - AllErr
	for n in range(len(AllFlux)):
		mask = (z2==z[n])*(x2==x[n])
		if sum(mask)==1:	#case of matching xz value exist:
			(ind,)= np.nonzero(mask)
			ind = ind[0]
			ThmFlux[n] = AllFlux[n]-FastFlux[ind]
			ThmErr [n] = quadrature(ary([AllErr[n],FastErr[ind]]))
		else:	#case of no matching xz value in the fast flux distribution
			ThmFlux[n] = AllFlux[n]
			ThmErr[n]  = AllErr [n]
	xz = append_axis(x,z)
	return xz, ThmFlux, ThmErr
def mymesh(x,y):
	mesh = ary(np.meshgrid(y,x)[::-1]).T	#reversed in direction so that the z stands up properly.
	return np.concatenate( mesh )#concatenation removes one dimension from the ary
	#in the shape of ((len(x)*len(y)),2)
	#i.e. in coordinate pairs listed.
def offdiag(matrix):
	assert matrix.ndim==2
	assert len(matrix)==len(matrix[0])#ensure it is a square matrix
	offdiagElem = []
	for i in range (len(matrix)):
		for j in range(i,len(matrix)-1):
			offdiagElem.append(matrix[i,j+1])
	return offdiagElem
def readData(inFile,y_val):
	df = pd.read_csv(inFile,delimiter="\t",header=1)
	dfxlen=len(df["x"])	#shortening the variable
	x = ary([df["x"][n]			for n in range(dfxlen)	if df["y"][n]==y_val])
	z = ary([df["z"][n]			for n in range(dfxlen)	if df["y"][n]==y_val])
	count = ary([df["counts"][n] for n in range(dfxlen)	if df["y"][n]==y_val])
	time = ary( [df["time"][n]  for n in range(dfxlen)	if df["y"][n]==y_val])
	
	count_err=ary([sqrt(cnt) for cnt in count])
	CntRate   = count/time
	CntRateErr= count_err/time
	return x,z,CntRate, CntRateErr
	#Operating in cgs units
	#ignoring x error and z error
def ToDataFrame(xz,Flux,FluxErr):
	xz = ary(xz)
	Flux = ary(Flux)
	FluxErr = ary(FluxErr)
	assert xz.ndim==2 and xz.shape[1]==2
	assert xz.shape[0]==Flux.shape[0]
	assert xz.shape[0]==FluxErr.shape[0]
	x,z = xz.T
	df = pd.DataFrame(ary([x,z,Flux,FluxErr]).T,columns=["x","z","flux","err"])
	return df
def RemoveData(xz,Flux,FluxErr,z_llim,z_ulim=200):
	xz = ary(xz)
	Flux = ary(Flux)
	FluxErr = ary(FluxErr)
	assert xz.ndim==2 and xz.shape[1]==2
	assert xz.shape[0]==Flux.shape[0]
	assert xz.shape[0]==FluxErr.shape[0]
	x,z = xz.T
	ind_ary = ary([ n for n in range(len(xz)) if z_llim<=z[n]<z_ulim ])
	assert len(ind_ary)>0, "no z fit these limit!"
	return xz[ind_ary],Flux[ind_ary],FluxErr[ind_ary]
def RemoveDatax(xz,Flux,FluxErr,x_llim,x_ulim):
	xz = ary(xz)
	Flux= ary(Flux)
	FluxErr = ary(FluxErr)
	assert xz.ndim==2 and xz.shape[1]==2
	assert xz.shape[0]==Flux.shape[0]
	assert xz.shape[0]==FluxErr.shape[0]
	x,z = xz.T
	ind_ary = ary([ n for n in range(len(xz)) if x_llim<=x[n]<x_ulim ])
	assert len(ind_ary)>0, "no x fits these limits!"
	#print(ind_ary)
	return xz[ind_ary],Flux[ind_ary],FluxErr[ind_ary]
def RemoveDataPoint(xz,Flux,FluxErr,x_rm,z_rm):
	xz = ary(xz)
	Flux= ary(Flux)
	FluxErr = ary(FluxErr)
	assert xz.ndim==2 and xz.shape[1]==2
	assert xz.shape[0]==Flux.shape[0]
	assert xz.shape[0]==FluxErr.shape[0]
	x,z = xz.T
	ind_ary = ary([ n for n in range (len(xz)) if (x[n]!=x_rm or z[n]!=z_rm) ])
	assert len(ind_ary)==(len(xz)-1), "more than 1 point removed from the xzdata!!"
	return xz[ind_ary],Flux[ind_ary],FluxErr[ind_ary]
def shiftxz(x,z,pivotedDF):
	xmin = min(pivotedDF.columns.values)
	zmin = min(pivotedDF.index)
	return x-xmin, z-zmin
#flux modelling methods:
def rShortHand(tau=False):
	if not tau:
		text = r"$\frac{ exp(- \frac{r}{a} ) } {r}$"
	else:
		text = r"$\frac{ exp(- \frac{r}{\sqrt{\tau}} ) } {r}, \tau = 368 cm^2$"
	text+= "\n where "+r"r=$\sqrt{x^2+y^2+z^2}$"
	return text
def Spherical(xz, L,target_y):	#just gonna fit it to Fast data once;
	xyz = add_y(xz,target_y)#so I use τ instead of L^2
	r = ary([quadrature(xyz) for xyz in xyz])
	spherical_unity = np.exp(-r/L)/r	#normalization constant = 1
	return spherical_unity
def Square(xz, L,α):
	[x,z] = xz.T
	Thm = cos(pi/(2*α)*x)* np.exp(-z*sqrt(pi*pi/(2*α*α)+1/(L*L)) )
	return Thm
def Square3(xz, L,α):
	[x,z] = xz.T
	Thm = (cos(pi/(2*α)*x)+cos(pi/(2*α)*3*x))* np.exp(-z*sqrt(pi**2/(α*α)*10/4+1/(L*L)) )
	return Thm
def Square9(xz, L,α):
	return Square(xz,L,α/3)
#shorthand for turning the fitting output into human readable information
def s(num):#turning a floating point number into a reader-friendly format
	assert isinstance(num,float)
	if 1<=log10(abs(num))<3:
		#10 -> 10.0
		#100->100.0
		#999->999.0
		string = "{:.1f}".format(num)
	elif 0<=log10(abs(num))<1 :
		#1  ->  1.00
		string = "{:.2f}".format(num)
	elif -1<=log10(abs(num))<0 :
		#0.1->  0.100
		string = "{:.3f}".format(num)
	else:
		string = ('%3.2e'%num)
		place  = string[-3:]#can only handle numbers between 10^+-100
		string = string[:-3]
		for char in place[:-1]:
			if (char!="+") and (char!="0"):
				string+=char
		string+= place[-1]
	return string
def f(num):
	assert isinstance(num,float)
	return str(num)[:6]
def fs(num):	#for creating xy labels
	num = float(num)
	num = "{:.1f}".format(num)
	return str(num)
#plotting subprograms
def residPlot(PlotObject1D,ax): #plotObject is expected to contain the following things:
	x_residual_err, equation= PlotObject1D#unpacking 1dplotObject
	x,resid,error=ary(x_residual_err).T #further unpacking
	#ax = fig.subplot(313)
	ax.errorbar(x,resid,error,fmt="o",ecolor="g",capsize=4, markersize=4, label=equation)
	#take care of the auxillary stuff
	ax.set_title("residuals")
	ax.set_xlabel("x (cm)")
	ax.legend()
	ax.axhline()
	return ax #may need tweaking to share the x-axis
	#eventually should make it into a plot object that can be stuck beneath the main graph.
def residPlot_constx(PlotObject1D,ax):
	z_residual_err, equation = PlotObject1D
	z,resid,error= ary(z_residual_err).T
	ax.errorbar(z,resid,error,fmt="o",ecolor="g",capsize=4,markersize=4, lable=equation)#wait what's that character
	ax.set_title("residuals")
	ax.set_xlabel("z (cm)")
	ax.legend()
	ax.axhline()
	return ax
def facetGrid(df,equation):#df must have the data columns ["x","z","diff","err"]
	sns.set(style="ticks", rc={"axes.facecolor": (0, 0, 0, 0)})
	# Create the data
	# Initialize the FacetGrid object
	row_order = df.z.unique()[::-1]#[101.25,81.0,60.75,40.5,20.25]
	#print(row_order)
	pal = sns.cubehelix_palette(7,light= 0.75,dark=0.5,rot=1.6,start=0.2,reverse=True)
	g = sns.FacetGrid(df, row="z",row_order=row_order, hue="z",aspect =4, palette=pal, height=2)
	g.map(plt.fill_between, "x","diff") #clip_on=False, alpha=1, lw=1.5, bw=.2)
	g.map(plt.errorbar,"x","diff","errbar",fmt="o",barsabove=True,ecolor="black",capsize = 10)
	g.map(plt.axhline, y=0, lw=2, clip_on=False)
	# Define and use a simple function to label the plot in axes coordinates
	def label_row(x, color, label):
		ax = plt.gca()
		ax.text(0, .2, "z="+label, fontweight="bold", color=color,
			ha="left", va="center", transform=ax.transAxes)
	g.map(label_row, "x")
	#Set the subplots to overlap
	g.fig.subplots_adjust(hspace=-.3)
	##Remove axes details that don't play well with overlap
	#g.set(yticks=[])
	#g.set(xticks=[])
	equation = g.fig.text(0.5,.6,equation)
	#g.invert_yaxis()
	#I know I can do this instead of doing the above [::-1] thing;
	#But it ain't broke, so I ain't fixing it.
	g.set_titles("")
	g.despine(bottom=True, left=False)
	#g.savefig("Printable/"+title+"_Residual.png")
	return g, equation
def variablePFunction(func,xdata,popt):
	numParam = len(popt)
	if numParam==0:
		return func(xdata)
	if numParam==1:
		return func(xdata,popt[0])
	if numParam==2:
		return func(xdata,popt[0],popt[1])
	if numParam==3:
		return func(xdata,popt[0],popt[1],popt[2])
	if numParam==4:
		return func(xdata,popt[0],popt[1],popt[2],popt[3])
	else:
		raise ValueError("Bruh there's too many variables in the model, are you sure you want to do that?")
def abbrName(longname):
	assert type(longname)==str
	abbFilename = longname.replace("Neutron flux distribution ","")
	abbFilename = abbFilename.replace("neutron flux distribution ","")
	abbFilename = abbFilename.replace("at ","")
	abbFilename = abbFilename.replace(" cm","")
	#abbFilename = abbFilename.replace("y","-")
	abbFilename = abbFilename.replace("alized ","")
	abbFilename = abbFilename.replace("Thermal","Thm")
	#abbFilename = abbFilename.replace(".png","")
	return abbFilename
'''
#abandoned piece of code from fluxFit.py
def xzThreshold(x_rm,z_rm):
	assert type(x_rm)==float and type(z_rm)==float
	global xzfast,FastFlux,fastFErr, xzThm,ThmFlux,ThmErr
	xzThm,ThmFlux,ThmErr =RemoveDataPoint(xzThm,ThmFlux,ThmErr,x_rm,z_rm)
	return
'''