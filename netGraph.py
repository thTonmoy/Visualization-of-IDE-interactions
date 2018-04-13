import inline as inline
import numpy as np
import pandas as pd
from pylab import rcParams, matplotlib
import seaborn as sb
import matplotlib.pyplot as plt
import networkx as nx
import csv
from mpl_toolkits.mplot3d import Axes3D


hackerRank_numericMapping = pd.read_csv('data/HackerRank-Developer-Survey-2018-Numeric-Mapping.csv')

netGraph = hackerRank_numericMapping
netGraph.plot()

plt.xlabel ('Occupation')
plt.ylabel ('Number of people')
plt.title("Network Graph")
plt.legend()

plt.show()
