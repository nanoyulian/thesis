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
        '''
    first glocal minimum found: 35
[ 4967  8569  7767 16687 14080  8853  6140  8678 14795  3150 11415  8581
  6308 10073  2529  1345 15565  8582  1405 11451 14867  7249 14908  8618
 10554  1797   350 16079 13619  6439  4825  8355  2506 12925 12384]'''