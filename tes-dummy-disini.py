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
from matplotlib import pyplot as plt

plt.rcParams['figure.figsize'] = (16, 9)
plt.style.use('ggplot')

#start_node = np.array([1,2]) - 1
#print start_node
#
#v = np.zeros(6)
#print v
#print len(v)
#
#u = np.zeros(6)
#print u
#print len(u)
#
#X = np.array(list(zip(u, v))) # bentuk matriks (bxk) dari pasangan u,v (6 x 2)
#print X
#print len(X) # jumlah baris
#
#v[start_node] = 1. / len(start_node)
#print v 
#
#
#for j in range(30):
#        v2 = deepcopy(v)
#        print v2
#
#x = [('a',2),('b',7)]
#print len(x)
#for i in x :
#    print ("%s" % str(i))

''' 8853 8582 350 1405 1797 6439 14867 = 7/8

 6308 10073       14908    16079 
  4825  8355  2506 12925 12384

first glocal minimum found: 35
[ 4967  8569  7767 16687 14080  6140  
  8678 14795 11415  8581 15565   11451   7249   8618
  10554  13619 3150 1345 2529 ]
'''

''' CONTOH CLUSTERING DENGAN K-MEANS '''
def distance(a,b, ax=1):
    return np.linalg.norm(a - b, axis=ax) 

#X adalah kumpulan data titik 2 dimensi yang ingin di cluster ke 2 centroid K = 2 :(0,1)
X = np.array([[11,12],[8,4],[4,7],[5,5],
              [9,2],
              [3,4],
              [4,6],
              [3,9],
              [1,5],
              [5,8],
              [6,0]] )

print X #format matrix

plt.scatter(X[:,0],X[:,1], c='black', s=7)


k = 2 # jumlah baris/data
# X coordinates of random centroids
C_x = np.random.randint(0, np.max(X)-1, size=k)
#print C_x
# Y coordinates of random centroids
C_y = np.random.randint(0, np.max(X)-1, size=k)
#print C_y
C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
print(C) #print matriks format ndarray
#print(C.shape) #bentuk/ordo matriks (bxk) (2x2)
#print(C.size) #jumlah data dalam matriks (2x2 = 4)
#print(len(C)) #jumlah baris = 2
#print C[0] #print baris ke 1 dari matriks
#print C[1] #print baris ke 2

# Plotting along with the Centroids
plt.scatter(X[:,0],X[:,1], c='#050505', s=7)
plt.scatter(C_x, C_y, marker='*', s=200, c='g')

C_old = np.zeros(C.shape) # matriks 2x2
# siapkan label cluster untuk semua data pada X, dalam format matriks. default 0 dari (0,1)
clusters = np.zeros(len(X))
# error fungsi untuk centroid lama dan baru (rata-2)
error = distance(C,C_old,None)


while error != 0:
    for i in range(len(X)):
            #hitung jarak 1 data terhadap semua centroid, 
            #buat mencari data tersebut nantinya lebih dekat ke centroid mana
            distances = distance(X[i], C)
            print "jarak ", X[i], "dengan", C, "=", distances
            #ambil index dari jarak terkecil pada distances
            cluster = np.argmin(distances) 
            #simpan hasil mapping index cluster untuk tiap data           
            clusters[i] = cluster
            #print "jarak terpendek titik ",X[i]," yaitu pd centroid ke- (0-1) : ", cluster
    print "Hasil awal cluster dari data X adalah : \n", clusters        
    
    # Storing the old centroid values
    C_old = deepcopy(C)
    
    #membuat centroid baru berdasarkan rata-rata dari tiap data per cluster dari clustering sebelumnya         
    for i in range(k):
        points = []        
        for j in range(len(X)):
            if clusters[j] == i :
                points.append(X[j])        
        #simpan titik centroid baru (replace) dari Mean/rata2x titik/ data 
        C[i] = np.mean(points, axis=0)    
        #print points      
        #print C[i]
    #membandingkan dengan yang centroid yang lama
    error = distance(C,C_old,None) 
    print error
    #error = 0 #SEHARUSNYA PILIH SAMPAI LEVEL ERROR = 0 ATAU CENTROID TIDAK BERUBAH KONVERGEN... 
    print "\n"
    
    #coloring data based on cluster above
    colors = ['r', 'g', 'b', 'y', 'c', 'm']
    fig, ax = plt.subplots()
    for i in range(k):
        points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
        ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
        ax.scatter(C[:, 0], C[:, 1], marker='*', s=200, c='#050505')

''' AKHIR DARI CONTOH K-MEANS CLUSTERING '''