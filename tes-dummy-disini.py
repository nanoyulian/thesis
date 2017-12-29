# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 06:41:05 2017

@author: nano
"""
#
#graph_linklist = [set() for i in range(0,100)]
#print graph_linklist
#
#for i in range(100):
#    graph_linklist[i].add(i)
#    
#print graph_linklist

from copy import deepcopy
import numpy as np

start_node = np.array([1,2]) - 1
print start_node

v = np.zeros(6)
print v

v[start_node] = 1. / len(start_node)
print v 

for j in range(30):
        v2 = deepcopy(v)
        print v2