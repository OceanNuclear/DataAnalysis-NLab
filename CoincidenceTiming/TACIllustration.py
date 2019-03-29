#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt


x=np.linspace(0,1.208,1209)

fig,ax = plt.subplots()
Figure = "TAC"

if Figure=="TAC":
	#Create other distributions
	mask=np.less_equal(x,1)
	y=mask*x
	
	#Make plot
	ax.plot(x,y,label="ss")

	#Set x axes
	ax.set_xticks([0,1])
	ax.set_xticklabels(["0","0.5"])
	ax.set_xlabel(r"time difference between the start and stop pulses ($\mu s$)")
	
	#set y axis
	ax.set_yticks([0,1])
	ax.set_yticklabels([0,10])
	ax.set_ylabel("amplitude of the TAC output pulse (V)")
# ax.legend()
fig.set_size_inches(4,3)
plt.savefig(Figure+".png",bbox_inches="tight")#Necessary for saving the thing properly
# plt.show()
print("Saved "+Figure+".png")
