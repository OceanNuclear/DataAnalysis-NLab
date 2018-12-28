#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import seaborn as sns
#fluxFit.py only deals with reading data and then fitting them.
from handleFit import *
#Oh my god the order matters:
#if you import handleFit AFTER flusDist, then you'll get into a loopy mess.
#But the current configuration works, i.e. BEFORE.
from fluxDists import *	#import the models to fit the data against.
from HiddenSubprograms import *	#other lower level programs
from matplotlib.ticker import FormatStrFormatter
import matplotlib.ticker as ticker
#print("fluxFit",__name__)
global FastFlux,fastFErr, ThmFlux,ThmErr, τ
τ = 368	#unit:cm^2

target_y=0	#picking the xz plane that contains the source.
print("for y=",target_y)
x,z, AllFlux, allFErr = readData("n-Diff-new.csv",y_val=target_y)
x2,z2,FastFlux,fastFErr=readData("CadmiumNew.csv",y_val=target_y)
xzfast = ary([x2,z2]).T#of shape (36,2)
xzThm,ThmFlux,ThmErr = Extended_thermal_flux(x,z,AllFlux,allFErr,x2,z2,FastFlux,fastFErr)
def zThreshold(llim=0, ulim= 200):
	global xzfast,FastFlux,fastFErr, xzThm,ThmFlux,ThmErr
	fast_1dpl,fast_0dpl=101.25,141.75
	xzThm,ThmFlux,ThmErr = RemoveData(xzThm,ThmFlux,ThmErr,llim,ulim)
	if (llim<=fast_0dpl):
		xzfast,FastFlux,fastFErr=RemoveData(xzfast,FastFlux,fastFErr,llim, ulim)
		if (llim>fast_1dpl):
			#raise ImportWarning("only one datapoint parsed for fast")
			print("Warning: only one data point parsed for fast neutron flux.")
	return
def xThreshold(llim=-61, ulim=61):
	global xzfast,FastFlux,fastFErr, xzThm,ThmFlux,ThmErr
	xzThm,ThmFlux,ThmErr	=RemoveDatax(xzThm,ThmFlux,ThmErr,llim,ulim)
	xzfast,FastFlux,fastFErr=RemoveDatax(xzfast,FastFlux,fastFErr,llim, ulim)
	return
def zT(ind):
	Slice = [(20.0,21.0),(40.0,41.0),(60.0,61.0), (80.0,82.0),(101.0,102.0),(141.0,142.0),(182.0,183.0)]
	low,upp=  Slice[ind]
	zThreshold(low,upp)
def xT(ind):
	Slice = [(-61.0,-60.0),(-41.0,-40.0),(-21.0,-20.0),(-1.0,1.0),(20.0,21.0),(40.0,41.0),(60.0,61.0)]
	low,upp=  Slice[ind]	
	xThreshold(low,upp)
def zCutoff(ind):
	if ind>=0:
		zThreshold((20.0,40.0,60.0,80.0)[ind])
	elif ind<0:
		zThreshold(llim=0,ulim=(25.0,45.0,65.0,85.0)[-ind])
def scaleUpError(SF):
	global fastFErr, ThmErr
	fastFErr, ThmErr = FastFlux*SF, ThmErr*SF
	return
def SquareError():
	global fastFErr, ThmErr
	fastFErr, ThmErr = FastFlux**2, ThmErr**2
	return 
#_______________________________________________CHANGE THE FOLLOWING
#zT(0)
#xT(3)
zCutoff(1)
SF=.70
#SquareError()
#scaleUpError(10);SquareError()#;scaleUpError(5)
#_______________________________________________END of changeable stuff


if __name__=="__main__":
	smoothData, plotObject=handleFittingResult(
	FastSquare,  xzfast,FastFlux,fastFErr, [368,77]);				titleName="Fast neutron flux distribution"
	#FastSquare_τ,xzfast,FastFlux,fastFErr, [77]);					titleName="Fast neutron flux distribution"
	#FastSph,     xzfast,FastFlux,fastFErr, [368]);					titleName="Fast neutron flux distribution \nwith spherically symmetric fit"
	#FastSph_τ,   xzfast,FastFlux,fastFErr,[]);						titleName="Fast neutron flux distribution \nwith spherically symmetric fit"
	#OneGrp_Thm, xzThm,ThmFlux,ThmErr,	[60,77]);					titleName="Thermal neutron flux distribution \nwith 1 group fit"
	#TwoGrp_Thm, xzThm,ThmFlux,ThmErr,	[60,77]);					titleName="Thermal neutron flux distribution \nwith 2 group fit with fixed τ"
	#TwoGrp_redefine_τ,xzThm,ThmFlux,ThmErr, [60,368,77]);			titleName="Thermal neutron flux distribution \nwith 2 group fit with"
	#OneGrp_Thm_Sph,xzThm,ThmFlux,ThmErr,[160]);					titleName="Thermal neutron flux distribution \nwith 1 group spherically symmetric fit"
	#ThirdOrd_OneGrp_Thmz,xzThm,ThmFlux,ThmErr,[160,0.4,77]);		titleName="Thermal neutron flux distribution \n1 group fit with 3rd order term"
	#ThirdOrd_TwoGrp_Thmz,xzThm,ThmFlux,ThmErr,[160,368,0.4,77]);	titleName="Thermal neutron flux distribution \n2 group fit with 3rd order term"
	#FixL,		xzThm,	ThmFlux,	ThmErr,	[0.2]);					titleName="Thermal neutron flux distribution \n1 group fit with 3rd order term"
	#FixLtau,	xzThm,	ThmFlux,	ThmErr,	[0.2]);					titleName="Thermal neutron flux distribution \n2 group fit with 3rd order term"
	#OneGrp_ThmNoBD, xzThm, ThmFlux, ThmErr, [55,20]);				titleName="Thermal neutron flux distribution \nwith 1 group fit"
	#GreensFuncFast,	xzfast, FastFlux,fastFErr, [76,368,121]);	titleName="Sinusoidal Summation for\n fast neutron flux distribution"
	#GreensFunc,		xzThm, ThmFlux, ThmErr, [76,368,121,60]);	titleName="Sinusoidal Summation for\n thermal neutron flux distribution"
	titleName+=' at y='+str(target_y)+" cm"
	fileName=abbrName(titleName)
	FAST =(("Fast" in fileName) or ("fast" in titleName))
	if FAST:
		heatmapDF = ToDataFrame(xzfast,FastFlux,fastFErr)
	else:
		heatmapDF = ToDataFrame(xzThm, ThmFlux, ThmErr  )
	x,z,flux,err = heatmapDF.values.T #resuing the x,z variables for more important things
	
	print( "Normalization constant=", f(readA()) )
	smoothData = pd.DataFrame(smoothData,columns=["x","z","flux"])
	if (heatmapDF.nunique()["z"]>1) and (heatmapDF.nunique()["x"]>1):
		#plotObject is a graph itself
		(plotObject,equation) = plotObject
		#set the title
		ttl_txt = plotObject.fig.suptitle("Residuals for fit "+get_expression())#,fontsize=20)#,xy=[.15,.8])
		if "set figure size"=="set figure size":
			fig_size = (plotObject.fig.get_size_inches())
			fig_size = fig_size*SF
			plotObject.fig.set_size_inches(fig_size)
		if heatmapDF.min()["z"]!=20.25:
			plotObject.savefig("Printable/"+fileName+" HeatMap with cutoff of z≥"+str(heatmapDF.min()["z"])+" cm RESIDUAL.png",dpi=100)
		else:
			plotObject.savefig("Printable/"+fileName+" HeatMap RESIDUAL.png",dpi=100)
		if "to clear figure"=="to clear figure":	#indented for clarity
			plt.cla()
			ttl_txt.set_text("")
			equation.set_text("")
		ax = plt.subplot(111)
		#plot the actual fit (in heat map form)
		smoothflux = smoothData.pivot("z","x","flux")
		smooth_x, smooth_z = np.meshgrid(smoothflux.columns.values,smoothflux.index)
		#Two cmaps to choose from, both from seaborn:
		#cmap = sns.diverging_palette(250, 15, s=75, l=40, center="dark",as_cmap=True)
		if not FAST:	#thermal neutron color palette
			cmap = sns.blend_palette(["b","r"],as_cmap=True)
		elif FAST:
			cmap = sns.blend_palette(["g","y"],as_cmap=True)
		heat = ax.pcolor(smooth_x,smooth_z,smoothflux, cmap=cmap)
		scat = ax.scatter(x,z,c=flux,cmap=cmap,edgecolor="w")
		cbar = plt.colorbar(heat,drawedges=False,ax=ax)
		if "formatting"=="formatting":# can remove anytime if I don't like the formatting:
			ax.set_xlabel("x (cm)")
			ax.set_ylabel("z (cm)")
			ax.axis([x.min()-1, x.max()+1, z.min()-1, z.max()+1])
			plt.tight_layout()
			for spine in ax.spines.values():
				spine.set_visible(False)
			cbar.outline.set_visible(False)
			cbar.set_label("counts/s")
			plt.figtext(0.5,0.001,"Background =best fit; colored dots = actual data.",wrap=True,ha="center")
			ax.set_title(titleName,va="top")
		if heatmapDF.min()["z"]!=20.25:
			fileName = "Printable/"+fileName+" HeatMap with cutoff of z≥"+str(heatmapDF.min()["z"])+" cm.png"
		else:
			fileName = "Printable/"+fileName+" HeatMap.png"
		plt.rcParams["figure.figsize"] = fig_size
		#plt.set_size_inches(fig_size)
		plt.savefig(fileName,dpi=100)
	elif (heatmapDF.nunique()["z"]==1):
		smoothData = smoothData.drop("z",axis=1)
		#smoothx,smoothy = smoothData.drop("z",axis=1).values.T
		fig,(fit,resid) = plt.subplots(2,1, gridspec_kw={'height_ratios':[3,2]})
		resid = residPlot(plotObject,resid)	#plot the residual
		smoothData.plot(x="x", y="flux" ,label = get_expression() , ax=fit, sharex=resid)
		#must unpack like this because DataFrame doesn't allow errorbar plot directly.
		z_str = f(heatmapDF["z"][0])
		fit.errorbar(x,flux,err, label="z="+z_str+"cm", fmt="o",ecolor="g",capsize=4, markersize=4)
		#take care of the auxillary stuff
		fit.legend()
		fit.set_ylabel(r"count rate ($s^{-1}$)")
		fit.set_title(titleName,)#va="top")
		fit.set_ylim(0)
		if "scaling"=="scaling":
			fig_size = fig.get_size_inches()
			fig_size = fig_size*SF
			fig.set_size_inches(fig_size)
		fileName="Printable/"+fileName+" z="+z_str+".png"
		fig.savefig(fileName)
	else:
		assert heatmapDF.nunique()["x"]==1
		smoothData = smoothData.drop("x",axis=1)
		#smoothx,smoothy = smoothData.drop("z",axis=1).values.T
		fig,(fit,resid) = plt.subplots(2,1, gridspec_kw={'height_ratios':[3,2]})
		resid = residPlot(plotObject,resid)	#plot the residual
		smoothData.plot(x="z", y="flux" ,label = get_expression() , ax=fit, sharex=resid)
		x_str = f(heatmapDF["x"][0])
		fit.errorbar(z,flux,err, label="x="+x_str+"cm", fmt="o",ecolor="g",capsize=4, markersize=4)
		fit.legend()
		fit.set_ylabel(r"count rate ($s^{-1}$)")
		fit.set_title(titleName,)#va='top')
		fit.set_ylim(0)
		resid.set_xlabel("z(cm)")
		if "scaling"=="scaling":
			fig_size = fig.get_size_inches()
			fig_size = fig_size*SF
			fig.set_size_inches(fig_size)
		fileName= "Printable/"+(fileName)+" x="+x_str+".png"
		fig.savefig(fileName)
	print("fileName=",fileName)
	'''
	bugs to fix: 
			2.0 make sure smooth heat map is in the correct direction, may have to tweak the [::-1] in mymesh	#DONE
			2. Put the actual data on top of heat map	#DONE
			2.1 using	#DONE
			ax.scatter()	#DONE
			2.2 Ensure that there are no text overlaps
			#2.3 Remove the text and title that has remained in the background of ax
			#Fixed using https://stackoverflow.com/questions/10559144/matplotlib-suptitle-prints-over-old-title
			2.3 format the ytick and xtick.	#DONE
			1. Make the program work for only a single slice of z data as well.
			1.0 Make sure mymesh works with zero as well.#DONE
			1.1 make sure that it prints out one graph (i.e. the following line should work:)
			1.2 with no overlap* text, and good layout	#DONE
			1.3 Legend should be readable	#DONE
	In fluxDists:
			1.6 Add units on cbar 	#DONE
			1.7 add captions using	#DONE
			1.4 make another batch of models that have exponential part replaced by 1	#DONE
			1.5 And redirect the current models to those ones when they detect that len(z.unique())==1	#DONE
			1.9 Carefully look through every single text expression for the fit equation used.
			1.9.2But where is that implemented???
			1.9.3 make an equivalent method of xthreshold; and deal/w /understand line 62 in handleFit.py #DONE
	1.8 Think about the title+their placements
	4. Make the actual plot, using a color scheme "b/r" for thermal, and a color scheme "g/y" for fast
	'''
else:
	print("End of importing! Weeee_______________________________________")