#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

# d=10
d=2.95
a=7.62/2
h=sqrt(a**2+d**2)#hypotenuse of the right angle triangle formed by a and d.
numTests=200000

#outdated version, replaced by the subprogram distList below.
# def distance(u,v):
# 	#finds the distance between two vectors, u and v
# 	difference = ary(u-v)
# 	answer = sqrt(np.sum(difference**2))
# 	return answer

def distList(uList,vList):
	# assert np.shape(uList)[0]==3 #tests to check that inputs were of the right shapes.
	# assert np.shape(vList)[0]==3	#These test were disabled after debugging has finished.
	difference=uList-vList
	diffsq= np.square(difference)
	diffsqsum=np.sum(diffsq,axis=0)
	# assert np.shape(vList)[1]==len(diffsqsum)
	distanceList=sqrt(diffsqsum)
	return distanceList

#outdated version, replaced by the subprogram InCircleList below.
# def InCircle(theta,phi,centroid_phi_displacement):
# 	#check if the point (theta, phi) falls inside the circle or not.
# 	r0=spherical_cartesian(pi/2,centroid_phi_displacement)
# 	r1=spherical_cartesian(theta,phi)
# 	r_max=sqrt(2)* sqrt(1-d/h)#which should be a scalar
	
# 	if distance(r0,r1)<=r_max:
# 		return True
# 	else:
# 		return False

def InCircleList(thetaList,phiList,centroid_phi_displacement):
	#thetaList and phiList are expected to be of the same shape.
	numList= len(thetaList)
	pi2    = pi/2*np.ones(numList)	#lengthen it into a list of the same shape
	PHIDISP= centroid_phi_displacement*np.ones(numList)
	
	r0List=spherical_cartesian(pi2,PHIDISP)
	r1List=spherical_cartesian(thetaList,phiList)
	#r_max is the maximum distance between the centre of the "circle" to the test vector r1 such that r1 still lies within the "circle", i.e.  the "radius" of the circle , in 3d.
	r_max =sqrt(2)* sqrt(1-d/h)#which should be a scalar
	#The formula for r_max is analytically derived; derivation not included in this code.

	distanceList=distList(r0List,r1List)
	TruthArray=np.less_equal(distanceList,r_max)
	return TruthArray

def Overlap(THETA):
	#THETA is the angle separating the centre of the two 'circles'.
	sumOverlap=0
	thetaList,phiList=[],[]
	
	for i in range (numTests):
		thetaList.append(rnTheta())
		phiList.append(rnPhi())
	thetaList,phiList=ary([thetaList, phiList])
	
	TruthArray1=InCircleList(thetaList,phiList,0)
	TruthArray2=InCircleList(thetaList,phiList,THETA)
	#multiplication of the two boolean arrays is equilvalent to using the "and" condition
	TotalValidAnswer=TruthArray1*TruthArray2

	return sum(TotalValidAnswer)/numTests

def rnTheta():
	u=np.random.uniform(-1,1)
	return arccos(u) #theta ranges from 0 to pi.

def rnPhi():
	return np.random.uniform(0,tau)

def spherical_cartesian(theta, phi):	#simple conversion from spherical coordinates to unit cartesian vectors
	x = sin(theta)*cos(phi)
	y = sin(theta)*sin(phi)
	z = cos(theta)
	return ary([x,y,z])

if __name__=="__main__":
	y=[]
	for x in range (0,91):
		print("computing for", x,"degree(s)")
		y.append(Overlap(np.deg2rad(x)))
	plt.plot(y)
	plt.xlabel("degrees")
	plt.ylabel("fraction of "+r"$\gamma$"+"'s detected by both detectors")
	plt.title("Angular variation by random number simulations")
	plt.show()
	f=open("AngularVariation.txt","w")
	[f.write(str(i)+"\n") for i in y]
	f.close()