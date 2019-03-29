#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt


x=np.linspace(0,1.4,140)

fig,ax = plt.subplots()
Figure = "epsilon"

if Figure=="epsilon":
	#Create other distributions
	y=x[::-1]
	y=np.clip(y,0,1)
	
	#Make plot
	ax.plot(x,y)

	#Set x axes
	ax.set_xticks([0,0.4])
	ax.set_xticklabels([r"$\approx 10keV$",r"$\approx$100keV"])
	ax.set_xlabel(r"$log(E_{\gamma})$")
	
	#set y axis
	ax.set_yticks([])
	ax.set_ylabel(r"$log(\epsilon_{abs})$")
# ax.legend()
fig.set_size_inches(4,3)
plt.title("approximate trend of detection efficiency of NaI")
# plt.show()
plt.savefig(Figure+".png",bbox_inches="tight")#Necessary for saving the thing properly
print("Saved "+Figure+".png")
