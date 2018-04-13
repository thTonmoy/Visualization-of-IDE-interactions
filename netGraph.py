import inline as inline
import numpy as np
import pandas as pd
from pylab import rcParams, matplotlib
import seaborn as sb
import matplotlib.pyplot as plt
import networkx as nx
import csv
from mpl_toolkits.mplot3d import Axes3D

import plotly.plotly as py
from plotly.graph_objs import *
import warnings

G=nx.Graph()

#extract and add AGE_GROUP nodes in graph
f1 = csv.reader(open("data/netGraph/user_agegroup.txt","r"))
for row in f1:
    G.add_nodes_from(row, color = 'blue')

#extract and add COUNTRY nodes in graph
f2 = csv.reader(open('data/netGraph/user_country.txt','r'))
for row in f2:
    G.add_nodes_from(row, color = 'red')

#extract and add USER_ID nodes in graph
f3 = csv.reader(open('data/netGraph/user_id.txt','r'))
for row in f3:
    G.add_nodes_from(row, color = 'yellow')

f4 = csv.reader(open('data/netGraph/id,agegroup.txt','r'))
for row in f4:
    if len(row) == 2 : # add an edge only if both values are provided
        G.add_edge(row[0],row[1])

f5 = csv.reader(open('data/netGraph/id,country.txt','r'))
'''
for row in f5:
    if len(row) == 2 : # add an edge only if both values are provided
        G.add_edge(row[0],row[1])
        '''
# Remove empty nodes
for n in G.nodes():
    if n == '':
        G.remove_node(n)
# color nodes according to their color attribute
color_map = []
for n in G.nodes():
    color_map.append(G.node[n]['color'])
nx.draw_networkx(G, node_color = color_map, with_labels = True, node_size = 500)

plt.savefig("path.png")

plt.show()






'''
warnings.filterwarnings('ignore')

G = nx.Graph(day="Stackoverflow")
df_nodes = pd.read_csv('data/HackerRank-Developer-Survey-2018-Numeric-Mapping.csv')
df_edges = pd.read_csv('data/HackerRank-Developer-Survey-2018-Numeric-Mapping.csv')

for index, row in df_nodes.iterrows():
    G.add_node(row['name'], group=row['group'], nodesize=row['nodesize'])

for index, row in df_edges.iterrows():
    G.add_weighted_edges_from([(row['source'], row['target'], row['value'])])

color_map = {1: '#f09494', 2: '#eebcbc', 3: '#72bbd0', 4: '#91f0a1', 5: '#629fff', 6: '#bcc2f2',
             7: '#eebcbc', 8: '#f1f0c0', 9: '#d2ffe7', 10: '#caf3a6', 11: '#ffdf55', 12: '#ef77aa',
             13: '#d6dcff', 14: '#d2f5f0'}

plt.figure(figsize=(25, 25))
options = {
    'edge_color': '#FFDEA2',
    'width': 1,
    'with_labels': True,
    'font_weight': 'regular',
}
colors = [color_map[G.node[node]['group']] for node in G]
sizes = [G.node[node]['nodesize'] * 10 for node in G]

"""
Using the spring layout : 
- k controls the distance between the nodes and varies between 0 and 1
- iterations is the number of times simulated annealing is run
default k=0.1 and iterations=50
"""
nx.draw(G, node_color=colors, node_size=sizes, pos=nx.spring_layout(G, k=0.25, iterations=50), **options)
ax = plt.gca()
ax.collections[0].set_edgecolor("#555555")
plt.show()

'''