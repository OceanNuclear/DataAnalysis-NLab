#!/home/ocean/anaconda3/bin/python3
#Method of use: go into the relevant directory where the 'Calib.txt' is stored, then run this .py file from that directory by prepending the appropriate pwd.
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
import seaborn as sns

SCALED = False
def Readxydy(fileName):
	f = open (fileName,'r')
	data = f.readlines()
	f.close()

	x,y,dy,labels=[],[],[],[]
	for line in data:
		if line.startswith("#"):
			prevLabel = line.replace("\n","").replace("#","")
		elif line!="\n":#if line is not empty
			line = line.split("\t")
			x.append (line[0])
			y.append (line[1])
			dy.append(line[2])
			labels.append(prevLabel)
	x = ary(x,dtype=float)
	y = ary(y,dtype=float)
	dy = ary(dy,dtype=float)
	if SCALED:
		dy = dy*sqrt(504)
	return (x,y,dy,labels)
def Continuous(x):
	return np.linspace(min(x),max(x),100, endpoint=True)

(x,y,dy,labels)=Readxydy('Calib.txt')
#(x,y,dy,labels)=Readxydy('Calib_A.txt')
#(x,y,dy,labels)=Readxydy('Calib_B.txt')

fit = np.polyfit(x,y,1, w=dy**(-2),cov=True )#w=dy**(-1), ) #Cheekily using 1/dy instead of 1/dy^2 because I feel like it's a bit too serious
global p
p,V = fit
print(np.diag(V))
print(V)
fitFunc = np.poly1d(p)
#Create plot
dummy, (ax1, ax2) = plt.subplots(2, sharex=True,gridspec_kw={'height_ratios':[3,2]})
#plt smooth function
xsm = Continuous(x)
ysm = fitFunc(xsm)
ax1.plot(xsm,ysm,label=str(fitFunc)[2:], )

setl = list(set(labels))
pal = sns.color_palette( n_colors= len(setl) )
def getColor(string):
	ind = setl.index(string)
	return pal[ind]
for n in range(len(x)):
	c = getColor(labels[n])
	ax1.errorbar(x[n],y[n],dy[n],fmt='.',label=labels[n], color=c)
def s(num):
	return '%s' % float('%.3g' % num) #two significant numbers!
covar = "Covariance matrix=\n" \
	+s(V[0,0])+"   "+s(V[0,1])+'\n' 	\
	+s(V[1,0])+"   "+s(V[1,1])
ax1.text(min(x),max(y), covar ,va="top",ha="left")#on the top left hand corner
if 'Auxillary stuff'=='Auxillary stuff':#indented to look nice
	#Auxillary stuff around the plot
	#plt.suptitle("gain=500")
	ax1.set_title("Calibration equation")
	ax1.set_ylabel("channel")
	ax2.set_xlabel("Energy(keV)")
	ax1.legend()
if "residual"=="residual":
	resid = y-fitFunc(x)
	chisq= sum( (resid/dy)**2 )/( len(x)-2 )#per DoF
	chisqstr= r'$\chi^2 =$'+str(chisq)
	ax2.errorbar(x,resid,dy,fmt='.')
	ax2.axhline(color="black",label=chisqstr)
	if not SCALED:
		ax2.legend()
plt.show()

def inverseFunc(Y):
	m = p[0]
	c = p[1]
	X = (1/m)*Y - c/m
	return X
while False:
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
