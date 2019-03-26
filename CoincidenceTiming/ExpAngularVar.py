#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
polar=True
distance="20cm"
# fname="CloseCounts.txt";titletext="Angular variation of count rate at 2.95cm away from the source"
# fname="FarCounts.txt"; titletext="Angular variation of count rate at 20cm away from the source"
# fname="AngularVariationd=2.95.txt"; titletext="Expected Angular variation at 2.95cm away\nfrom source by random number simulations"
fname="AngularVariationd=20cm.txt"; titletext="Expected Angular variation at 20cm away\nfrom source by random number sampling"
if distance=="20cm":
	fnameList=["FarCounts.txt","AngularVariationd=20cm.txt"]
	labels=iter(["Recorded count rate","Expected Angular variation (calculated)"])
elif distance=="2.95cm":
	fnameList=["CloseCounts.txt","AngularVariationd=2.95cm.txt"]
	labels=iter(["Recorded count rate","Expected Angular variation (calculated)"])
for fname in fnameList:
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
	if "Angular" in fname:
		count_rate=multiplier*count_rate/max(count_rate)
	multiplier = max(count_rate)
	if polar:
		count_rate=np.concatenate([count_rate[::-1],count_rate])
		deg=np.deg2rad(np.concatenate([-x[::-1],x]))
		plt.polar(deg,count_rate,marker="x")
		plt.fill_between(deg,count_rate,0,alpha=0.4,label=next(labels))
	else:
		plt.xlabel("Angle")
		plt.plot(x,count_rate,marker="x",label=next(labels))
if polar:
	plt.xticks([-pi/2,0])
	# plt.xtickslabel(["pi/2","0","-pi/2"])
plt.ylim(bottom=0)
plt.legend()
plt.title("Comparison of experimental count rate vs expected count rate\n at source separation="+distance)
plt.ylabel("Count rate"+r"${s}^{-1}$")
plt.show()