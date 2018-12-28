#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
import matplotlib.pyplot as plt
import pandas as pd
import matplotlib.colors as colors
#from scipy.interpolate import interp2d
#from scipy.interpolate import Rbf
from matplotlib import cm
from scipy.interpolate import griddata

#declaring constants
batch = 49
start=0*batch
end = 1*batch-1
xStep = 100
yStep = 200

#file reading part
inFile = "n-Diffusion-BF3Measurement.csv"
df= pd.read_csv(inFile, sep="\t", header=1)
xdata = df.x[start:end]
ydata = df.y[start:end]
zdata = df.z[start:end]
counts = df.CountRate[start:end]

#rbf = Rbf(r, d, counts/100, epsilon=2)
#zi = rbf(ri, di)
#interpolation
x, y = np.mgrid[min(xdata):max(xdata):1j*xStep, min(ydata):max(ydata):1j*yStep]
dtpt = ary([xdata,ydata]).T
counts = griddata(dtpt, (counts/100), (x, y), method='linear')

fig = plt.figure()
ax = fig.add_subplot(111)
graph = ax.pcolor(x,y,counts, cmap=cm.jet)
#plt.scatter(x, y, 100, counts, cmap=cm.jet)
ax.set_aspect('equal')
#fig = plt.pcolormesh(x,y,counts)

plt.xlabel("x/cm")
plt.ylabel("y/cm")
plt.title("Heat Map of Count")

plt.colorbar(graph, label = "Count Rate (/s)")

#plt.show(block=False) #going to find a way to show it before saving via terminal input
saveName = "HeatMapPlotDraft"
#saveName = input("Enter save file name:")
saveName+=".png"
plt.savefig(saveName)