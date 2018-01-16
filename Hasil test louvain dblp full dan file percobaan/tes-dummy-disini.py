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
import networkx as nx  
import random as rand
#
#plt.rcParams['figure.figsize'] = (16, 9)
#plt.style.use('ggplot')

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
#
##X adalah kumpulan data titik 2 dimensi yang ingin di cluster ke 2 centroid K = 2 :(0,1)
#X = np.array([[11,12],[8,4],[4,7],[5,5],
#              [9,2], [3,4], [4,6],[3,9],
#              [1,5], [5,8], [6,0]] )
#
#print X #format matrix
#
#plt.scatter(X[:,0],X[:,1], c='black', s=7)
#
#
#k = 2 # jumlah baris/data
## X coordinates of random centroids
#C_x = np.random.randint(0, np.max(X)-1, size=k)
##print C_x
## Y coordinates of random centroids
#C_y = np.random.randint(0, np.max(X)-1, size=k)
##print C_y
#C = np.array(list(zip(C_x, C_y)), dtype=np.float32)
#print(C) #print matriks format ndarray
##print(C.shape) #bentuk/ordo matriks (bxk) (2x2)
##print(C.size) #jumlah data dalam matriks (2x2 = 4)
##print(len(C)) #jumlah baris = 2
##print C[0] #print baris ke 1 dari matriks
##print C[1] #print baris ke 2
#
## Plotting along with the Centroids
#plt.scatter(X[:,0],X[:,1], c='#050505', s=7)
#plt.scatter(C_x, C_y, marker='*', s=200, c='g')
#
#C_old = np.zeros(C.shape) # matriks 2x2
## siapkan label cluster untuk semua data pada X, dalam format matriks. default 0 dari (0,1)
#clusters = np.zeros(len(X))
## error fungsi untuk centroid lama dan baru (rata-2)
#error = distance(C,C_old,None)
#
#
#while error != 0:
#    for i in range(len(X)):
#            #hitung jarak 1 data terhadap semua centroid, 
#            #buat mencari data tersebut nantinya lebih dekat ke centroid mana
#            distances = distance(X[i], C)
#            print "jarak ", X[i], "dengan", C, "=", distances
#            #ambil index dari jarak terkecil pada distances
#            cluster = np.argmin(distances) 
#            #simpan hasil mapping index cluster untuk tiap data           
#            clusters[i] = cluster
#            #print "jarak terpendek titik ",X[i]," yaitu pd centroid ke- (0-1) : ", cluster
#    print "Hasil awal cluster dari data X adalah : \n", clusters        
#    
#    # Storing the old centroid values
#    C_old = deepcopy(C)
#    
#    #membuat centroid baru berdasarkan rata-rata dari tiap data per cluster dari clustering sebelumnya         
#    for i in range(k):
#        points = []        
#        for j in range(len(X)):
#            if clusters[j] == i :
#                points.append(X[j])        
#        #simpan titik centroid baru (replace) dari Mean/rata2x titik/ data 
#        C[i] = np.mean(points, axis=0)    
#        #print points      
#        #print C[i]
#    #membandingkan dengan yang centroid yang lama
#    error = distance(C,C_old,None) 
#    print error
#    #error = 0 #SEHARUSNYA PILIH SAMPAI LEVEL ERROR = 0 ATAU CENTROID TIDAK BERUBAH KONVERGEN... 
#    print "\n"
#    
#    #coloring data based on cluster above
#    colors = ['r', 'g', 'b', 'y', 'c', 'm']
#    fig, ax = plt.subplots()
#    for i in range(k):
#        points = np.array([X[j] for j in range(len(X)) if clusters[j] == i])
#        ax.scatter(points[:, 0], points[:, 1], s=7, c=colors[i])
#        ax.scatter(C[:, 0], C[:, 1], marker='*', s=200, c='#050505')

''' AKHIR DARI CONTOH K-MEANS CLUSTERING '''


''' PERCOBAAN SPECTRAL CLUSTERING SEDERHANA ''' 
#import community as co
#''' Graph awal '''
#G = nx.Graph()
#G.add_edge(0,1)
#G.add_edge(1,2)
#G.add_edge(2,3)
#G.add_edge(3,4)
#G.add_edge(4,5)
#G.add_edge(5,6)
#G.add_edge(6,7)
##G.add_edge(1,8)
#G.add_edge(0,6)
#G.add_edge(5,7)
#G.add_edge(3,6)
#G.add_edge(2,0)
#
#G.add_edge(9,10)
#G.add_edge(10,11)
#G.add_edge(11,12)
#G.add_edge(12,13)
#G.add_edge(13,14)
#G.add_edge(14,15)
#G.add_edge(15,16)
#G.add_edge(9,16)
#G.add_edge(10,13)
#G.add_edge(9,8)
#''' visualisasi graph '''
#plt.figure(1)
#nx.draw_networkx(G,pos=nx.spring_layout(G), width = 0.6, edge_color="#ff0000", node_color="#333399",alpha=0.4, node_size=10)
#''' Dari Graph ke Adj. Matrix A '''
#A = nx.to_numpy_matrix(G,dtype=int)
#''' Compute Degree Matrix A '''
## hitung degree tiap baris di matriks A
#d = np.matrix.sum(A, axis=0)
## siapkan matriks kosong size A
#D = np.zeros(np.shape(A),int)
## masukkan degree vertex jadi diagonal di mat D
#np.fill_diagonal(D,d)
#''' hitung Laplacian Matrix L = D - A unnormalized '''
#L = D - A
#''' Eigenvalues Decomposition : hitung eigenvalues and eigenvector ''' 
## untuk eigvect setiap kolom adalah eigevect1, eighvect2 , dst... 
#eigval, eigvect = np.linalg.eig(L)
#''' urutkan eigenvalues, ambil yang kedua terkecil dan ambil eigen vector yang bersangkutan '''
#sorted_eigval = sorted(eigval)
## plotting sorted eigenvalues
#plt.figure(2)
#rank_eigval = []
#for i in range(len(sorted_eigval)): 
#    rank_eigval.append(i+1)
#  
#plt.plot(rank_eigval,sorted_eigval,'bo')
#
#plt.grid(True)
## set label untuk axis (horizontal X)
#plt.xlabel('Ranking EigenValue (1 - n)')
## set label untuk axis (Vertikal Y)
#plt.ylabel('EigenValue')
##convert to list
#list_eigval = np.ndarray.tolist(eigval)
## ambil indeks  dari eigenvalue yg ke dua dari eigval : idx_second_smallest_eigval
#idx_second_smallest_eigval = list_eigval.index(sorted_eigval[1])
## ambil indeks  dari eigenvalue yg ke dua dari eigval : idx_second_smallest_eigval
#idx_first_smallest_eigval = list_eigval.index(sorted_eigval[0])
## ambil indeks  dari eigenvalue yg ke dua dari eigval : idx_second_smallest_eigval
#idx_third_smallest_eigval = list_eigval.index(sorted_eigval[2])
## ambil indeks  dari eigenvalue yg ke dua dari eigval : idx_second_smallest_eigval
#idx_fourth_smallest_eigval = list_eigval.index(sorted_eigval[3])
## ambil eigenvector 2nd smallest dari index eigval bersangkutan : berada pada eigvect dgn index 9 
#second_smallest_eigvect = eigvect[:,idx_second_smallest_eigval]
## 4 eigenvector terkecil utk jadi 4 cluster
#fourth_smallest_eigvect = eigvect[:,[idx_first_smallest_eigval,idx_second_smallest_eigval,idx_third_smallest_eigval,idx_fourth_smallest_eigval]]
#
## 3 eigenvector terkecil utk jadi 4 cluster BANDINGKAN dengan Louvain
#third_smallest_eigvect = eigvect[:,[idx_first_smallest_eigval,idx_second_smallest_eigval,idx_third_smallest_eigval]]
#
#'''dari second smallest eigenvector lakukan grouping berdasarkan median 0 ''' 
##clustA = []
##clustB = []
##i = 0
##for x in second_smallest_eigvect:
##    if x < 0.0 :
##        clustA.append(i) # negatif eigenvector
##    else:
##        clustB.append(i) # positif eigenvector
##    i = i+1
## Hasil cek Manual dengan median 0
##clustB=[0,1,3,4,5,6,7,10,11,12,13,16,17,19,21]
##clustA=[2,8,9,14,15,18,20,22,23,24,25,26,27,28,29,30,31,32,33]
#
##color_map = []
##for node in G:
##    if node in clustA:
##        color_map.append('blue')
##    else: color_map.append('green')  
##    
##nx.draw(G,node_color = color_map,with_labels = True)
##plt.show()
#
### put together a color map, one color for a category
#                   
#''' compute k-means dari eigvector maksimal 4 cluster(percobaan)''' 
#from sklearn.cluster import KMeans
#k = 3
#kmeans = KMeans(n_clusters=k, random_state=0).fit(fourth_smallest_eigvect)
#print kmeans.labels_
#
#color_map = []
#for c in kmeans.labels_: 
#    if c == 0:
#        color_map.append('b')
#    elif c == 1:
#        color_map.append('y')
#    elif c == 2:
#        color_map.append('g')
#    else:
#        color_map.append('r')
#plt.figure(3)
#nx.draw(G,pos=nx.spring_layout(G),node_color = color_map,with_labels = True)
#
#''' LOUVAIN ALGORITHM '''
#print "running Louvain Algorithm..."
#part = co.best_partition(G)
##bikin part baru iterate, yang urutannya sesuai dengan g.nodes￼
#part2 = [] #list baru
##print list(G)
#for x in G.nodes():
#    part2.append(part[x])
#
##set color for each community
#part_id = [ float((_x+1)) for _x in part2]
#colors = [ (_i/(_i+3)) for _i in part_id] 
#
##draw graph and apply the colors for each community.
#plt.figure(4)
##nx.draw_networkx(G,node_color = colors,  with_labels=True, alpha=0.5, node_size=18 )
#nx.draw_networkx(G,pos=nx.spring_layout(G), node_color = colors)
#
#plt.show()

#''' Nyoba Sorting '''
#def getKey(item):
#    return item[1]
#
#a = [['nano',3], ['kambing',1], ['dina',3], ['andin',8], ['nindy',5]]
#
#print "jumlah member a : ", len(a)
#a.sort(key=getKey, reverse = True)
#print "member a dgn degree terbesar : ", a[0:3]
#

d = {'nano':1, 'dina':2, 'andin':3, 'icha' : 4, 'nindy' : 5}
print d['nano']


