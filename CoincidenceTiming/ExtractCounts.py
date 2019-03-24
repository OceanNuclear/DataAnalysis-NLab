#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
import glob

PathToGrep="/home/ocean/Documents/GitHubDir/DataAnalysis-NLab/CoincidenceTiming/11-30/22Na*.Spe"
paths=glob.glob(PathToGrep)
paths.sort()
f=open("AllCounts_old.txt","w")

for path in paths:
	p=open(path,"r")
	data=p.readlines()
	data = [ int(x) for x in data[12:2060] ]
	data = data[:]
	count=sum(data)
	p.close()
	
	fname=path.split("/")[-1]
	fname=fname.replace("22Na-Coin-511Window-fullrange0_5us10V_","")
	fname=fname.replace(".Spe","")
	
	f.write(fname+"\t"+str(count)+"\n")
f.close()