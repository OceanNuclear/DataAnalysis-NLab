#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt
f = open ('Calib.txt','r')
data = f.readlines()
f.close()
x,y,dy=[],[],[]
for line in data:
	line = line.split("\t")
	x.append (line[0])
	y.append (line[1])
	dy.append(line[2])
