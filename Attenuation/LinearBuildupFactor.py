#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
f=  open("Uncol.txt","r")
data = f.readlines()
f.close()

Thickness, Build, dBuild= [],[],[]
for line in data:
	if len(line)>1:
		xval, yval, yerr= line.split("\t")
		Thickness.append(xval)
		Build.append(yval)
		dBuild.append(yerr)
Thickness, Build, dBuild= ary([Thickness, Build, dBuild],dtype=float)
plt.errorbar(Thickness,Build,dBuild)
plt.title("Buildup factor in collimated geometry")
plt.xlabel("Thickness (mm)")
plt.ylabel("Buildup factor")

fitx= ary([Thickness[0]-0.5,Thickness[-1]+0.5])
opt,cov = np.polyfit(Thickness,Build,1, w=dBuild**(-2), cov=True )
m,c=opt
fity=m*fitx+c
plt.plot(fitx,fity,label="best fit line")
print("m=",m,"c=",c)
print(cov)
print("chi^2/DoF=",(np.sum( ((Build-(m*Thickness+c))/dBuild)**2 ))/(len(Thickness)-2))
plt.legend()
plt.savefig("BuildUpFactorLinearPlot.png",dpi=80)