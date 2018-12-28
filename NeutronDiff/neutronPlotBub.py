#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
import matplotlib.pyplot as plt
import pandas as pd

inFile = "n-Diffusion-BF3Measurement.csv"
#inFile = "CadmiumNew.csv"
batch = 49
start=0*batch
end = 3*batch-1

df= pd.read_csv(inFile, sep="\t", header=1)
x = df.x[start:end]
y = df.y[start:end]
z = df.z[start:end]
counts = df.CountRate[start:end]
for i in range (len(x)):
	print(x[i],y[i],z[i],df.time[i],counts[i],df.CountRate[i], sep="\t")
exit()
plt.scatter(x,z, s=(counts*0.02))
plt.xlabel("x/cm")
plt.ylabel("z/cm")
plt.title("Bubble plot of Count rate")
plt.show()