# -*- coding: utf-8 -*-
"""
Created on Thu Dec 28 06:41:05 2017

@author: nano
"""

graph_linklist = [set() for i in range(0,100)]
print graph_linklist

for i in range(100):
    graph_linklist[i].add(i)
    
print graph_linklist