#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

cnt=[]
ax=plt.subplot()
def PropErr(x1,dx1,x2,dx2):
	y=x1/x2
	#fractional error: (dy/y)**2 = (dx1/x1)**2+(dx2/x2)**2
	dy=sqrt((dx1/x1)**2+(dx2/x2)**2)*y
	return y,dy
f=open("Sources.txt")
sources=f.readlines()
f.close()
#Separated into Sources.txt (only store source relevant info) and Efficiency.txt (Only stores count relevant info + intensity of each peak)

def disPerSec(isot):
	for line in sources:
		if isot == line.split()[0]:
			line = line.replace("\n","").split("\t")
			isot=line[0].replace("#","")
			time,OldAct, OldErr,days,halfl=ary(line[1:6],dtype=float)
			if len(line)>6:
				Act,ActErr=ary(line[6:8], dtype=float)
		#need to compare the calculated result against the existing number, do they fall within a margin?
	factor=2**(-days/halfl)
	Disin_calc,DisinErr_calc=time*ary([OldAct,OldErr])*factor #activity left * duration of recording
	#And print them
	if 'error checking'!="error checking":
		Disin,DisinErr=	ary([Act,ActErr])*time
		print("isot",isot)
		print("Disin",Disin,Disin_calc)
		print("DisinErr",DisinErr,DisinErr_calc)
	return Disin_calc, DisinErr_calc
if __name__=="__main__":
	f = open("Efficiency.txt")
	data = f.readlines()
	f.close()
	for line in data:
		if not (line.startswith("#") or len(line)<=3):
			line = line.split("\t")
			E.append(  line[0])
			cnt.append(line[1])
			err.append(line[2])
			Int.append(line[3])
		else:
			if len(cnt)!=0:
				E,cnt,err,Int=ary([E,cnt,err,Int],dtype=float)
				#Do some numerical processing
				Disin,DisinErr=disPerSec(t.split()[0])
				#</numerical processing>
				efficiency,error=PropErr(cnt,err,Disin,DisinErr)
				plt.errorbar(E,efficiency,error,label=t,  linestyle='',marker="x",markersize=4,capsize=3)
			t=line[1:-1]
			E, cnt, err, Int = [], [], [], []
	# ax.set_xscale("log", nonposx='clip')
	# ax.set_yscale("log", nonposy='clip')
	plt.legend()
	plt.show()