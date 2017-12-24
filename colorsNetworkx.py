# -*- coding: utf-8 -*-
"""
Created on Tue Nov  7 16:55:25 2017

@author: nano
"""

import networkx as nx
import matplotlib.pyplot as plt
from random import random
g = nx.random_graphs.erdos_renyi_graph(10,0.5)
colors = [(random(), random(), random()) for _i in range(10)]
print random()
nx.draw_circular(g, node_color=colors)
plt.show()