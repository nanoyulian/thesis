# -*- coding: utf-8 -*-
"""
Thesis = Nano Y.P. 2017
Louvain in DBLP co-author networks

"""
import networkx as nx 
import csv as csv 
import matplotlib.pyplot as plt
import community as co
from itertools import count
from random import random

#open data input file with edge list format 
#f= open("co-author.csv")
f= open("com-amazon.csv")
df = csv.reader(f, delimiter = '\t' )
#initialize empty graph (networkX)
G = nx.Graph()

#Building a network, read edge list as row in file input
n=1
for row in df:
    if n<100: # number of row
        G.add_edge(row[0],row[1])        
        n=n+1
    else:
        break
    
#close file connection
f.close()

#call the louvain method and apply it in our network (G)
part = co.best_partition(G)

#sort part dictionary based on G.nodes()
#index_map = {v: idx for idx, v in enumerate(list(G),0)}
#print index_map
#print "\n"
#sorted(part.items(), key=lambda pair: index_map[pair[0]])

#bikin part baru iterate, yang urutannya sesuai dengan g.nodes
part2 = [] #list baru
#print list(G)
for x in G.nodes():
    part2.append(part[x])

#set color for each community
part_id = [ float((_x+1)) for _x in part2]
colors = [ (_i/(_i+3)) for _i in part_id]

#print "\n"
#print colors

#draw graph and apply the colors for each community.
nx.draw_networkx(G,node_color = colors,  with_labels=False, alpha=0.5, node_size=10 )
print "\n"
print "Modularity: ", co.modularity(part,G)
print "Num. Communities:",  len(set(part.values()))
print "Num. of Vertices:", G.number_of_nodes()
print "Num. of Edges: ", G.number_of_edges()
print "Network Size:", G.size()
plt.show()
