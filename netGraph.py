import csv

import matplotlib.pyplot as plt
import networkx as nx

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






