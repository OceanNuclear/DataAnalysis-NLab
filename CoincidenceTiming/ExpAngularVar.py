#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
polar=True
fname="CloseCounts.txt";titletext="Angular variation of count rate at 2.95cm away from the source"
# fname="FarCounts.txt"; titletext="Angular variation of count rate at 10cm away from the source"
# fname="AngularVariation.txt"; titletext="Expected Angular variation at 2.95cm away from source by random number simulations"
# fname="AngularVariation10cm.txt"; titletext="Expected Angular variation at 10cm away from source by random number simulations"

f=open(fname,"r")
data=f.readlines()
f.close()

x,y,z=[],[],[]
n=0
for line in data:
	line=line.split("\t")
	if len(line)>=2:
		x.append(line[0])
		y.append(line[1])
	if len(line)>2:
		z.append(line[2])
	else:
		assert len(line)==1
		x.append(n)
		y.append(line[0])
		n+=1
if z==[]:
	z=np.ones(len(data))
x,y,z=ary([x,y,z],dtype=float)
count_rate=y/z

if polar:
	count_rate=np.concatenate([count_rate[::-1],count_rate])
	deg=np.deg2rad(np.concatenate([-x[::-1],x]))
	plt.polar(deg,count_rate,marker="x")
	plt.fill_between(deg,count_rate,0)
	plt.xticks([-pi/2,0])
	# plt.xtickslabel(["pi/2","0","-pi/2"])
else:
	plt.xlabel("Angle")
	plt.plot(x,count_rate,marker="x")
plt.ylim(bottom=0)
plt.title(titletext)
plt.ylabel("Count rate"+r"${s}^{-1}$")
plt.show()