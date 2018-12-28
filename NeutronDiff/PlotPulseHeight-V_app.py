#!/home/ocean/anaconda3/bin/python3
from numpy import cos, arccos, sin, arctan, tan, pi, sqrt; from numpy import array as ary; import numpy as np; tau = 2*pi
from matplotlib import pyplot as plt; from matplotlib.ticker import ScalarFormatter
import pandas as pd

df= pd.read_csv("PulseHeight-V_app.csv", header=1, sep="\t", names=["V_app", "Min", "Max", "error"])
ax = plt.subplot(111)
ax.set_yscale("log")#nonposy="clip"
ax.errorbar(df.V_app, df.Max, yerr=df.error,capsize=3 , label="max pulse height")
ax.errorbar(df.V_app, df.Min, yerr=df.error,capsize=2.5,label="min pulse height")
ax.yaxis.set_major_formatter(ScalarFormatter())
ax.set_title("min/max pulse height vs applied voltage")
plt.legend()
plt.savefig("/home/ocean/Documents/NuclearAndMaterialsProjects/MScNuclearLab/Printable/Figure5-Min-Max-Plot.png")