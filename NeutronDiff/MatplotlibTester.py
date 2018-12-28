#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt

global var
def changevar():
	global var
	var = 1
	return
if __name__=="__main__":
	changevar()
	print(var)
'''
fig = plt.figure(2)
#fig is a blank slate sitting on top of a "canvas". Fig has dimension 640x480 pixels, and is absolutely useless on its own.
ax2 = fig.add_subplot(211)
ax2.plot([0,2,1])
#ax = fig.add_axes([0.05, 0.05, .92,.92])
ax = fig.add_subplot(312) #This configuration covers it
#ax is the window with fixed location and shape relative to the canvas.
##In the interactive interface you can drag around in the coordinate space;
##but the ax's relative position to the canvas will not change.
#ax2 = fig.add_axes([0.05, 0.05, .92,.92])
ax.plot([1,2,3])
#plt.show()
print(ax.fig)
'''