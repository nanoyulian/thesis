#!/usr/bin/env python
# encoding:UTF-8

################################################################################################
#
#    Community Detection via Local Spectral Clustering
#
################################################################################################

# (Our algorithm is also known as "LEMON", which is the short form of Local Expansion via Minimum One Norm)


# LEMON.py
# Yixuan Li
# Last modified: 2015-1-8
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version

import numpy as np
import math 
import pulp                       # You need to manually install this package in order to run this code
#import sys
#import random
import gc

from copy import deepcopy
#from scipy import io as spio
#from scipy import sparse
from scipy import linalg as splin
from optparse import OptionParser


def swap(a,b):
    if a > b:
        return b,a
    return a,b


def set_initial_prob(n,starting_nodes):
    """Precondition: starting_nodes is ndarray which indicate the indices of starting points 
       
       Return: A probability vector with n elements
    """
    v = np.zeros(n)
    v[starting_nodes] = 1./starting_nodes.size
   
    return v



def set_initial_prob_proportional(n,degree_sequence,starting_nodes):
    """Precondition: starting_nodes is ndarray which indicate the indices of starting points 
       
       Return: A probability vector with n elements
    """
    v = np.zeros(n)
    vol = 0
    for node in starting_nodes:
        vol += degree_sequence[node]
    for node in starting_nodes:
        v[node] = degree_sequence[node]/float(vol)

    return v


def read_edgelist(filename,delimiter=None,nodetype=int):
    """Generate the adjacent matrix of a graph with overlapping communities. 
       Input: A two-clumn edgelist 
       
       1 2
       1 3
       1 4
       ...
       ...
       
       Return: An adjacency matrix in the form of ndarray corresponding to the given edge list.
    """
    edgeset = set()
    nodeset = set()
    
    print "Reading the edgelist... nodeset : kumpulan node(label) yg udah di sort, edgeset : kumpulan edge pada graph" 
    with open(filename) as f:
        for line in f.readlines():
            if not line.strip().startswith("#"):
                L = line.strip().split(delimiter)
                ni,nj = nodetype(L[0]),nodetype(L[1])
                nodeset.add(ni) 
                nodeset.add(nj)                
                if ni != nj:
                    edgeset.add(swap(ni,nj)) # (1,2 )
                    
        node_number = len(list(nodeset))
        edge_number = len(list(edgeset))
        
        #print nodeset
        #print node_number
        #print edgeset 
    del edgeset
    
    print "The network has", node_number, "nodes with", edge_number, "edges."
    graph_linklist = [set() for i in range(0,node_number)]   # Initialize the graph in the format of linked list
    del nodeset
    
    #print graph_linklist
    
    for i in range(node_number):
        graph_linklist[i].add(i)
    
    #print graph_linklist
    
    with open(filename, 'U') as f: 
        for line in f.readlines():
            #print line
            if not line.strip().startswith("#"):
                L = line.strip().split(delimiter)
                ni,nj = nodetype(L[0]),nodetype(L[1])
                #print ni,nj
                if ni != nj:
                    a = ni - 1   #YANG DIPAKE ADALAH INDEXNYA BUKAN VALUENYA.... 
                    b = nj - 1
                    graph_linklist[a].add(b) # KENAPA FORMATNYA SEPERTI INI, MEMPERMUDAH HITUNG DEGREE
                    graph_linklist[b].add(a)
    gc.collect()

    degree = []
    for node in range(node_number):
        degree.append (len(graph_linklist[node])) #HITUNG DEGREE NYA SETIAP NODE HASIL KUMPULAN SET DR GRAPH_LINKLIST
        #print len(graph_linklist[node])

    print "Finish constructing graph."
    print "-------------------------------------------------------"
    
    #print graph_linklist
    
    return graph_linklist, node_number, edge_number,degree



def read_groundtruth(filename,delimiter=None,nodetype=int):
    """Input: a file with list of the nodes and their membership(s) (memberships are labelled by integer numbers >=1). 
       For example:  A      3 6 8 (Node A belongs to community 3, 6 and 8)
       Output: a nested list where each sublist correspondes to a community, containing the node indices within the community
    
    """
    comm_count = 12000
    print "Parsing ground truth communities..."
    communities = [[] for i in range(comm_count)]


    with open(filename, 'U') as f:
        count = 0
        for line in f.readlines():
            if not line.strip().startswith("#"):
                L = line.strip().split('\t')
                membership_array = np.fromstring(L[0],dtype=int,sep=' ')
                
                communities[count] = membership_array
                count += 1 
    print "Finish parsing communities."
    
   
    return communities, count



def adj_to_Laplacian(G):
    """Computes the normalized adjacency matrix of a given graph"""

    n = G.shape[0]
    D = np.zeros((1,n))
    for i in range(n):
        D[0,i] = math.sqrt(G[i,:].sum())

    temp = np.dot(D.T, np.ones((1,n)))
    horizontal = G / temp
    normalized_adjacency_matrix = horizontal / (temp.T)
    gc.collect()

    return normalized_adjacency_matrix


def cal_conductance(G,cluster):
    """cluster: a list of node id that forms a community. Data type of cluster is given by numpy array

       Calculate the conductance of the cut A and complement of A. 
    """

    assert type(cluster) == np.ndarray, "The given community members is not a numpy array"

    temp = G[cluster,:]
    subgraph = temp[:,cluster]
    cutsize = temp.sum() - subgraph.sum()
    denominator = min(temp.sum(),G.sum()-temp.sum())
    conductance = cutsize / denominator
  
    return conductance


def sample_graph(G_linklist,node_number,degree_sequence,starting_node,sample_rate=None,biased=True):
    
    initial = np.array(starting_node) #STARTING_NODE ADALAH ARRAY DARI SEED YG DIDIFENISIKAN SEBELUMNYA
    if biased:
        prob_distribution = set_initial_prob_proportional(node_number,degree_sequence,initial)
    else:
        prob_distribution = set_initial_prob(node_number,initial)

    subgraph = set(starting_node) #SUBGRAPH YANG DIHASILKAN DARI SET DARI SEEDSET 
    RW_graph = set(starting_node)
        
    for j in range(30):
        original_distribution = deepcopy(prob_distribution) #cloning dari objek prob_distribution
        for node in RW_graph:
            #print "node : ", node 
            neighbors = G_linklist[node]
            #print "len(neighbors) :" , len(neighbors)            
            divided_prob = original_distribution[node] / float(len(neighbors))
            #print "divided_prob: ", divided_prob            
            prob_distribution[node] -= original_distribution[node]
            #print "\n"
            for v in neighbors:
                prob_distribution[v] += divided_prob
            #ini yang merubah node di RW_Graph saat perulangan
            RW_graph = RW_graph.union(neighbors)
                        
            if len(RW_graph) >= 7000:
                break      
            
    #print G_linklist[100905]
    #print RW_graph
    
    for i in range(30): #KENAPA DIULANG 30X ??? Karena buat nyample buat distribusi sampelnya (neighbors)
        for node in subgraph:
            
            neighbors = G_linklist[node]
            subgraph = subgraph.union(neighbors)
           
            if len(subgraph) >= 7000:
                break
    
    #print RW_graph
    #print subgraph
    
    index = 0
    RW_dict = {}
    RW_dict_reverse = {}
    sub_prob_distribution = []
    for node in subgraph:
        RW_dict[node] = index   # mapping from whole graph to subgraph
        RW_dict_reverse[index] = node   # mapping from subgraph to whole graph
        sub_prob_distribution.append(prob_distribution[node])
        index += 1
    
    #new = [0 for k in range(node_number)] 
    new_graph_size = 3000 #jumlah node pada graph baru yang akan disample berdasarkan seed

    node_in_new_graph = list(np.argsort(sub_prob_distribution)[::-1][:new_graph_size])
    node_in_new_graph_ori_index = []
    for v in node_in_new_graph:
        node_in_new_graph_ori_index.append(RW_dict_reverse[v])
    node_in_new_graph_ori_index = set(node_in_new_graph_ori_index)
    
    #print "The size of sampled graph is", len(node_in_new_graph)
    new_graph = np.eye(new_graph_size)
    map_dict = {}
    map_dict_reverse = {}
    count = 0
    for i in range(node_number):
        if i in node_in_new_graph_ori_index:
            map_dict[count] = i   # from new to original
            map_dict_reverse[i] = count  # from original to new
            count += 1
  
    for i in range(new_graph_size):
        for j in range(new_graph_size):
                a = map_dict[i]
                b = map_dict[j]
                if a in G_linklist[b]:

                    new_graph[i,j] = 1.0
                    new_graph[j,i] = 1.0
    #print "new graph returned"
    sample_rate = new_graph_size / float(node_number)

    return new_graph, map_dict, map_dict_reverse, sample_rate, new_graph_size


def map_from_new_to_ori(nodelist,map_dict):
    """
    Given a list of node indices in the new graph after sampling, return the list of indices that the nodes correspond
    to in the original graph before sampling. 
    
    """
    nodelist = np.array(nodelist)
    mapped_list = []
    for node in nodelist:
        mapped_list.append(map_dict[node])

    return np.array(mapped_list)


def map_from_ori_to_new(nodelist,map_dict_reverse):
    """
    Given a list of node indices in the original graph before sampling, return the list of indices that the nodes correspond
    to in the new graph after sampling. 
    """
    nodelist = np.array(nodelist)
    mapped_list = []
    for node in nodelist:
        if node in map_dict_reverse:
            mapped_list.append(map_dict_reverse[node])
        else:
            mapped_list.append(10000000000)  # set the value to be infinity when the key cannot be found in the dictionary


    return np.array(mapped_list)


def random_walk(G,initial_prob,subspace_dim=3,walk_steps=3):
    """
    Start a random walk with probability distribution p_initial. 
    Transition matrix needs to be calculated according to adjacent matrix G.
    
    """
    assert type(initial_prob) == np.ndarray, "Initial probability distribution is \
                                             not a numpy array"
       
    # Transform the adjacent matrix to a laplacian matrix P
    P = adj_to_Laplacian(G)
    
    Prob_Matrix = np.zeros((G.shape[0], subspace_dim))
    Prob_Matrix[:,0] = initial_prob
    for i in range(1,subspace_dim):
        Prob_Matrix[:,i] = np.dot(Prob_Matrix[:,i-1], P)
     
    Orth_Prob_Matrix = splin.orth(Prob_Matrix)
    
    for i in range(walk_steps):
        temp = np.dot(Orth_Prob_Matrix.T, P)
        Orth_Prob_Matrix = splin.orth(temp.T)
    
    return Orth_Prob_Matrix


    
def min_one_norm(B,initial_seed,seed):

    weight_initial = 1 / float(len(initial_seed))
    weight_later_added = weight_initial / float(0.5)
    difference = len(seed) - len(initial_seed)
    [r,c] = B.shape
    prob = pulp.LpProblem("Minimum one norm", pulp.LpMinimize)
    indices_y = range(0,r)
    y = pulp.LpVariable.dicts("y_s", indices_y, 0)
    indices_x = range(0,c)
    x = pulp.LpVariable.dicts("x_s", indices_x)

    f = dict(zip(indices_y, [1.0]*r))

    prob += pulp.lpSum(f[i] * y[i] for i in indices_y) # objective function
    
    prob += pulp.lpSum(y[s] for s in initial_seed) >= 1

    prob += pulp.lpSum(y[r] for r in seed) >= 1 + weight_later_added * difference

    for j in range(r):
        temp = dict(zip(indices_x, list(B[j,:])))
        prob += pulp.lpSum(y[j] + (temp[k] * x[k] for k in indices_x)) == 0

    prob.solve()

    #print "Status:", pulp.LpStatus[prob.status]
    result = []
    for var in indices_y:
        result.append(y[var].value())
   
    return result 

def seed_expand_auto(G,seedset,min_comm_size,max_comm_size,expand_step=None,subspace_dim=None,walk_steps=None,biased=True):
  
    degree = []
    n = G.shape[0]
    for x in range(n):
        degree.append(G[x].sum())

    # Random walk starting from seed nodes:
    if biased:
        initial_prob = set_initial_prob_proportional(n, degree, seedset)
    else:
        initial_prob = set_initial_prob(G.shape[0], seedset)

    Orth_Prob_Matrix = random_walk(G,initial_prob,subspace_dim,walk_steps)
    initial_seed = seedset
    
    # Initialization
    detected = list(seedset)
    [r,c] = Orth_Prob_Matrix.shape #row, column
    seed = seedset 
    step = expand_step
    iteration = 0
    F1_scores = []
    Jaccard_scores = []
    detected_comm = []
   
    global_conductance = np.zeros(30)
    global_conductance[-1] = 1000000 # set the last element to be infinitely large
    global_conductance[-2] = 1000000
    flag = True

    F1_score_return = []
    Jaccard_score_return = []
    
    iteration = 0
    while flag:
        temp = np.argsort(np.array(min_one_norm(Orth_Prob_Matrix,list(initial_seed),list(seed))))
      
        sorted_top = list(temp[::-1][:step])
       
        detected = list(set(list(detected) + sorted_top))
        seed = np.array(detected)
               
        conductance_record = np.zeros(max_comm_size - min_comm_size + 1)
        conductance_record[-1] = 0
        community_size = [0]
        for i in range(min_comm_size,max_comm_size):
            candidate_comm = np.array(list(temp[::-1][:i]))
            conductance_record[i-min_comm_size] = cal_conductance(G,candidate_comm)
               
    
        detected_size, cond = global_minimum(conductance_record,min_comm_size)
           
        step += expand_step
        
        if biased:
            initial_prob = set_initial_prob_proportional(n, degree,seedset)
        else:
            initial_prob = set_initial_prob(G.shape[0], seedset)
       
        Orth_Prob_Matrix = random_walk(G,initial_prob,subspace_dim,walk_steps)
      
        if detected_size != 0: 
            current_comm = list(temp[::-1][:detected_size])
            detected_comm = current_comm
        
        else:
            F1_score = 0
            Jind = 0

        global_conductance[iteration] = cond
        if global_conductance[iteration-1] <= global_conductance[iteration] and global_conductance[iteration-1] <=global_conductance[iteration-2]:
            flag = False
           
        iteration += 1
    
    return detected_comm


def global_minimum(sequence,start_index):

    
    detected_size = len(list(sequence))
    seq_length = len(list(sequence))
    cond = sequence[seq_length-2]
    for x in range(40):
        list(sequence).append(0)
    for i in range(seq_length - 40):
        if sequence[i] < sequence[i-1] and sequence[i] < sequence[i+1]:
            count_larger = 0
            count_smaller = 0
            for j in range(1,32):
                if sequence[i+1+j] > sequence[i+1]:
                    count_larger += 1
            for k in range(1,32):
                if sequence[i-1-k] > sequence[i-1]:
                    count_smaller += 1
            if count_larger >= 18 and count_smaller >= 18:
                print "first glocal minimum found:",i + start_index
                detected_size = i + start_index
                cond = sequence[i]
                break
    return detected_size, cond
     

def cal_Fscore(detected_comm,ground_truth_comm,beta=1):
    """
        Given a set of algorithmic communities C and the ground truth communities S, F score measures the relevance 
        between the algorithmic communities and the ground truth communities. 
        F_beta = (1+beta^2) / beta^2 * (precision(S)*recall(S)) / (precision(S)+recall(S))
    """
    detected_comm = list(detected_comm)
    ground_truth_comm = list(ground_truth_comm)
    correctly_classified = list(set(detected_comm).intersection(set(ground_truth_comm)))
    precision = len(correctly_classified) / float(len((detected_comm)))
    recall = len(correctly_classified) / float(len(ground_truth_comm))
    if precision !=0 and recall != 0:
        Fscore = (1 + math.sqrt(beta)) / float(math.sqrt(beta)) * precision * recall / float(precision + recall)
    else:
        Fscore = 0

    return Fscore


def cal_Jaccard(detected_comm,ground_truth_comm):
    """
    Jaccard is defined as the size of the intersection divided by the size of the union of the sample sets

    """
    detected_comm = list(detected_comm)
    ground_truth_comm = list(ground_truth_comm)
    correctly_classified = list(set(detected_comm).intersection(set(ground_truth_comm)))
    union = list(set(detected_comm).union(set(ground_truth_comm)))
    Jind = len(correctly_classified) / float(len(union))

    return Jind


if __name__=='__main__':


#########################################################################################
    # Parse the arguments
    class MyParser(OptionParser):
        def format_epilog(self, formatter):
            return self.epilog
    
    usage = "usage: python LEMON.py [options]"
    description = """
    """
    epilog = """

    """
    parser = MyParser(usage, description=description,epilog=epilog)
    parser.add_option("-d", "--delimiter", dest="delimiter", default=' ',
                      help="delimiter of input & output files [default: space]")

    parser.add_option("-f", "--input network file", dest="network_file", default="../f2_edgelist_map_id",
                      help="input file of edge list for clustering [default: example_graphs/amazon/graph]")

#    parser.add_option("-g", "--input community ground truth file", dest="groundtruth_community_file", default="../example/amazon/community",
#                      help="input file of ground truth community membership [default: example_graphs/amazon/community]")

    parser.add_option("--out", "--output file", dest="output_file", default="output.txt",
                      help="output file of detected community [default: output.txt]")

    parser.add_option("--sd", "--input seed set file", dest="seed_set_file", default="../dblp_seed",
                      help="input file of initial seed set [default: example_graphs/amazon/seed]")

    parser.add_option("-c", "--minimum community size", dest="min_comm_size", default=50,
                      help="the minimum size of a single community in the network [default: 50]")

    parser.add_option("-C", "--maximal community size", dest="max_comm_size", default=100,
                      help="the maximum size of a single community in the network [default: 100]")

    parser.add_option("-s", "--sample rate", dest="sample_rate", default=0.007,
                      help="the percentile of nodes left for local detection after sampling [default: 0.007]")

    parser.add_option("-e", "--expand step", dest="expand_step", default=6,
                      help="the step of seed set increasement during expansion process [default: 6]")

    parser.add_option("-z", "--seed set size", dest="ini_num_of_seed", default=3,
                      help="the initial number of seeds used for expansion [default: 3]")


    (options, args) = parser.parse_args()
    delimiter = options.delimiter
    network_file = options.network_file
    #community_file = options.groundtruth_community_file
    output_file = options.output_file
    seed_set_file = options.seed_set_file
    min_comm_size = int(options.min_comm_size)
    max_comm_size = int(options.max_comm_size)
    sample_rate = float(options.sample_rate)
    expand_step = int(options.expand_step)
    seed_set_size = int(options.ini_num_of_seed)

  
####################################################################################################################

    #comms_indices_map, count = read_groundtruth(community_file,delimiter=delimiter,nodetype=int)
    graph_linklist,node_number,edge_number, degree = read_edgelist(network_file,delimiter=delimiter,nodetype=int)
    
    # write out result
    f = open('output_lemon','wb')
    f.write("#detected communities : (perbaris) \n")
    # read the initial seed set from file
    with open(seed_set_file) as fin:
        for line in fin.readlines():
            if not line.strip().startswith("#"):
                L = line.strip().split('\t')
                seedset = np.fromstring(L[0],dtype=int,sep=' ')
                print "Seed Set : " , seedset
                seedset = np.array(seedset) - 1
                 # sample the graph, adjust indices      PAKE METODE GRAPH SAMPLING (LIHAT DI PAPER), 
                # NEW GRAPH SUDAH DALAM BENTUK MATRIKS ADJANCCY MATRIKS DARI NODE-NODE YANG DISAMPLE
                #map_dict = mapping index antara (indexNode-newgraph : indexNode-graph asli)
                #new_seedset = INDEXNODE DARI INDEXNODE-NEWGRAPH => LIHAT hasil map_dict
                new_graph, map_dict, map_dict_reverse, sample_rate, new_graph_size  = sample_graph(graph_linklist,node_number,degree,seedset,0.007,biased=False)
                new_seedset = map_from_ori_to_new(seedset,map_dict_reverse)
                
                # run the local spectral clustering algorithm and return the detected community (Note: the indices here correspond to mapped indices in the sampled graph)
                detected_comm = seed_expand_auto(new_graph,new_seedset,min_comm_size,max_comm_size,expand_step,subspace_dim=3,walk_steps=6,biased=False)
                # map the indices back to the original graph
                detected_comm_ori = map_from_new_to_ori(detected_comm,map_dict)
                #ditambah 1 karena ini matrix dari INDEX node communitynya.. 
                # print detected_comm_ori + 1                 
                # hilangkan karakter awal n akhir
                str_q = str((list(detected_comm_ori+1) ))[1 : -1]
                #hilangkan spasi
                str_q.replace(" ", "")
                # write out result            
                f.write(str_q)    
                f.write("\n")
    #seedset = np.array(seedset) - 1 #get the index not the value
    f.close()
    
    # sample the graph, adjust indices      PAKE METODE GRAPH SAMPLING (LIHAT DI PAPER), 
    # NEW GRAPH SUDAH DALAM BENTUK MATRIKS ADJANCCY MATRIKS DARI NODE-NODE YANG DISAMPLE
    #map_dict = mapping index antara (indexNode-newgraph : indexNode-graph asli)
    #new_seedset = INDEXNODE DARI INDEXNODE-NEWGRAPH => LIHAT hasil map_dict
#    new_graph, map_dict, map_dict_reverse, sample_rate, new_graph_size  = sample_graph(graph_linklist,node_number,degree,seedset,0.007,biased=False)
#    new_seedset = map_from_ori_to_new(seedset,map_dict_reverse)
#    
#    # run the local spectral clustering algorithm and return the detected community (Note: the indices here correspond to mapped indices in the sampled graph)
#    detected_comm = seed_expand_auto(new_graph,new_seedset,min_comm_size,max_comm_size,expand_step,subspace_dim=3,walk_steps=6,biased=False)
#    # map the indices back to the original graph
#    detected_comm_ori = map_from_new_to_ori(detected_comm,map_dict)
#    #ditambah 1 karena ini matrix dari INDEX node communitynya.. 
#    print detected_comm_ori + 1 
#
#    # write out result
#    with open(output_file,"a") as out:
#        out.write("# detected community:"+"\n")
#        out.write(str(list(detected_comm_ori+1)))
#        out.write('\n')
       

"""
ALGORITMA LEMON

INPUT (edgelist,seed_node)
OUTPUT (DETECTED COMMUNITY)

1. Membangun Graph link List (edges di setiap node (degree))
2. New_Graph = Melakukan Graph Sampling berdasarkan Seed Node yang didefinisikan 
2a Bentuk adjancy Matriks dari new_graph
3. Lakukan Local Spectral Clustering pada Matriks New_Graph Berdasarkan 
   NewSeed Node dengan pendekatan random walk
4. Mendapatkan Komunitas pada New_Graph

Seeding Methods :
the inward-edge ratio for a vertex v is defined by 
the fraction of links connecting to another vertex inside the target community C 
among all the links coming out from v. 
We pick |S| vertices with inward-edge ratio ranked 
in the top one third among all vertices in C.

inward-edge ratio = jumlah edge dalam C (kecuali vertex v) / degree v  

PROPOSE PEMILIHAN SEED DENGAN MENGGUNAKAN LOUVAIN ALGORITHM
BAGAIMANA MEMILIH COMMUNITY AWAL UNTUK PROSES SEEDING ? 
    - LAKUKAN COMMUNITY DETECTION ALGORITHM MISAL LOUVAIN
    - PILIH 1/3 COMMUNITY DENGAN MEMBER TERBESAR 
    - PILIH 1/3 SEED DI TIAP COMMUNITY
        DAN UNTUK TIAP KOMUNITAS DILAKUKAN PEMILIHAN VERTEX SEED BERDASARKAN INWARD-EDGE RATIO
    

"""

















