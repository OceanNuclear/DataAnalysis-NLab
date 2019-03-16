#!/home/ocean/anaconda3/bin/python3
#Method of use: go into the relevant directory where the 'Calib.txt' is stored, then run this .py file from that directory by prepending the appropriate pwd.
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

f = open("Calib.txt")
data = f.readlines()
f.close()
#making empty lists
x,y,dy=[],[],[]#for fitting purpose
xp,yp,dp=[],[],[]#the sub-list that will hold each isotope's peaks info
xlong,ylong,zlong=[],[],[]#the overall lists that will add the
labels=[]
#creating emtpy graphs
dummy, (ax1, ax2) = plt.subplots(2, sharex=True,gridspec_kw={'height_ratios':[3,2]})
#Data reading
for line in data:
	if not( line.startswith("#") or len(line)<=3):#if line has data
		line = line.split("\t")
		xp.append(line[0])
		x.append (line[0])
		yp.append(line[1])
		y.append (line[1])
		dp.append(line[2])
		dy.append(line[2])
	else: #empty line or comment line, 
	 	if len(xp)!=0:
	 		xp,yp,dp = ary([xp,yp,dp],dtype=float)
		 	labels.append(t)
		 	xlong.append(xp)
		 	ylong.append(yp)
		 	zlong.append(dp)
	 		#ax1.errorbar(xp,yp,dp,label=t)
 		t=line[1:-1]
	 	xp,yp,dp=[],[],[]
#Converting into numpy.arrays
x = ary(x ,dtype=float)
y = ary(y ,dtype=float)
dy= ary(dy,dtype=float)
#(x,y,dy,labels)=Readxydy('Calib_A.txt')
#(x,y,dy,labels)=Readxydy('Calib_B.txt')
if "smooth bg"=='smooth bg':
	ax2.axhline(color="black")
	fit = np.polyfit(x,y,1, w=dy**(-2), cov=True )#w=dy**(-1), ) #Cheekily using 1/dy instead of 1/dy^2 because I feel like it's a bit too serious
	global p
	p,V = fit
	fitFunc = np.poly1d(p)
	#Create plot
	#plt smooth function
	def Continuous(x):
		return np.linspace(min(x),max(x),100, endpoint=True)
	xsm = Continuous(x)
	ysm = fitFunc(xsm)
	ax1.plot(xsm,ysm,label=str(fitFunc)[2:], )
if "errorbars"=="errorbars":
	for n in range(len(xlong)):
		ax1.errorbar(xlong[n],ylong[n],zlong[n],fmt='x',label=labels[n],capsize=3)
		if "residual"=="residual":
			resid = ylong[n]-fitFunc(xlong[n])
			ax2.errorbar(xlong[n],resid,zlong[n],fmt='x',capsize=3)

if 'axes texts'=='axes texts':
	#Auxillary stuff around the plot
	#plt.suptitle("gain=500")
	ax1.set_title("Calibration equation")
	ax1.set_ylabel("channel")
	ax2.set_xlabel("Energy(keV)")
	ax1.legend()
if 'covar'=='covar':
	def s(num):
		return '%s' % float('%.3g' % num) #two significant numbers!
	covar = "Covariance matrix=\n" \
		+s(V[0,0])+"   "+s(V[0,1])+'\n' 	\
		+s(V[1,0])+"   "+s(V[1,1])
	ax1.text(min(x),max(y), covar ,va="top",ha="left")#on the top left hand corner
plt.show()

def inverseFunc(Y):
	m = p[0]
	c = p[1]
	X = (1/m)*Y - c/m
	return X
while True:
	In = input("Energy or Channel number?")
	if In=="E":
		E = float(input("Energy = "))
		print(fitFunc(E))
	if In=="C":
		C = float(input("Channel = "))
		print(inverseFunc(C))
	if In=='q' or In=='Q':
		break
#Need to use scale up error bar code that makes chi^2 ==1
