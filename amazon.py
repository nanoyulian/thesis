# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:07:47 2018

@author: nano
"""

import json
import gzip
import itertools
import networkx as nx  
import matplotlib.pyplot as plt

def parse(path): 
    g = gzip.open(path, 'r') 
    for l in g: 
        yield json.dumps(eval(l))

#Menyimpan graph dalam format edgelist ke File (labelling dimulai dari 1)
def generate_edgelistfile(G, show_graph = False): 
    ''' Menyimpan graph dalam format edgelist ke file.
        [f1 : file edgelist dengan nama/id vertex asli,
        f2 : file edgelist dengan nama/id vertex dimulai dari 1,
        f3 : file keterangan hasil mapping id vertex pada f1 dgn f2] \n
        
        Parameter : \n
        show_graph : True/False (default: False), Menampilkan graph dari G (NetworkX) '''    
        
    print "Creating f3_nodes_id file..."
    f3=open('f3_nodes_id','wb')
    dict_id = {}
    #print G.nodes
    for key,val in zip(G.nodes,range(len(G.nodes))):
        dict_id[key]=val
        f3.write("%s : %d \n" % (key, val+1))
    f3.close()
    
    print "Creating f1_data and f2_edgelist file..."
    #print dict_id_authors['Andrade:Ewerton_R=']+1 = 336 (eurosp)
    f1=open('f1_edgelist_ori_id','wb')
    f2=open('f2_edgelist_map_id','wb')    
    
    for u,v in sorted(G.edges()):
        f1.write("%s %s\n" % (u, v))
        #convert tiap nama ke integer mulai dari 1 biar bisa dibaca di LEMON
        f2.write("%d %d\n" % (dict_id[u]+1,dict_id[v]+1) )
        
    f1.close()
    f2.close()
    
    if show_graph == True:
        plt.figure('Graph')
        plt.rcParams['axes.facecolor'] = '#ffffb3'
        nx.draw_networkx(G,pos=nx.spring_layout(G), width = 0.1, edge_color="#663300", node_color="#006600", with_labels=False,alpha=0.3, node_size=2)


#############################################################################################################################################################
if __name__ == "__main__":
    i = 0
    #idmap asin mapping buat asin ke integer mulai dari 1
    idmap_asin = 0
    #asin graph
    g_asin = nx.Graph()
    #telusuri setiap baris di file meta_Apps_for_Android.json.gz
    for l in parse("meta_Apps_for_Android.json.gz"):     
        #baca sampai baris ke - n
        #if i<20:
            #load baris ke dictionary data
            data = json.loads(l)
            #simpan value asin 
            asin = data["asin"]               
            #hanya ambil/proses baris yang ada key "related" nya saja
            if "related" in data : 
                #untuk setiap dictionary data (key, val)
                for key,val in data.items():
                    # pastikan val adalah dictionary dan val adalah nested key "also_bought" di setiap baris maka tulis edge 
                    if isinstance(val,dict):
                        if "also_bought" in val:
                            #simpan semua asin dalam key also_bought dalam format list
                            asin_bought = list(val["also_bought"])
                            #tambahkan asin utama ke list
                            asin_bought.append(asin) 
                            #menambahkan edge list ke dalam graph
                            for edge_list in asin_bought:
                                #print edge_list[0],edge_list[1]                            
                                g_asin.add_edge(asin,edge_list)   
                
                idmap_asin += 1
                
        #else:
        #    break
        #i +=1
    
    print "jumlah baris yg diproses : ", idmap_asin
    #print g_asin.nodes()    
    print "jumlah node : " , g_asin.number_of_nodes()
    print "jumlah_edge : " , g_asin.number_of_edges()
    
    ############ MUlai metain pake fungsi generate_edgelist #################
    generate_edgelistfile(g_asin, show_graph = True)

