#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

a=2.95
d=7.62
h=sqrt(a**2+d**2)
numTests=20000

def distance(u,v):
	#finds the distance between two vectors, u and v
	difference = ary(u-v)
	answer = sqrt(np.sum(difference**2))
	return answer

def InCircle(theta,phi,centroid_phi_displacement):
	#check if the point (theta, phi) falls inside the circle or not.
	r0=spherical_cartesian(pi/2,centroid_phi_displacement)
	r1=spherical_cartesian(theta,phi)
	r_max=sqrt(2)* sqrt(1-d/h)#which should be a scalar
	
	if distance(r0,r1)<=r_max:
		return True
	else:
		return False

def Overlap(THETA):
	#THETA is the angele separating the centre of the two circles.
	sumOverlap=0
	for i in range (numTests):
		testTheta=rnTheta()
		testPhi  =  rnPhi()
		if InCircle(testTheta,testPhi,0) and InCircle(testTheta,testPhi,THETA):
			sumOverlap+=1
	return sumOverlap/numTests

def rnTheta():
	u=np.random.uniform(-1,1)
	return arccos(u) #theta ranges from 0 to pi.

def rnPhi():
	return np.random.uniform(0,tau)

def cartesian_spherical(x, y, z):
	x,y,z = ary([x,y,z], dtype=float) #change the data type to the desired format

	Theta = arccos(np.clip(z,-1,1))
	Phi = arctan(np.divide(y,x))	#This division is going to give nan if (x,y,z) = (0,0,1)
	Phi = np.nan_to_num(Phi)	#Therefore assert phi = 0 if (x,y) = (0,0)
	Phi+= ary( (np.sign(x)-1), dtype=bool)*pi #if x is positive, then phi is on the RHS of the circle; vice versa.
	return ary([Theta, Phi])

def spherical_cartesian(theta, phi):	#simple conversion from spherical to cartesian, assuming r = 1
	x = sin(theta)*cos(phi)
	y = sin(theta)*sin(phi)
	z = cos(theta)
	return ary([x,y,z])
y=[]
for x in range (0,91):
	y.append(Overlap(np.deg2rad(x)))
plt.plot(y)
plt.xlabel("degrees")
plt.ylabel("fraction of gamma's detected by both detectors")
plt.show()