# -*- coding: utf-8 -*-
"""
Created on Tue Nov 21 09:48:39 2017

@author: nano
"""

from lxml import html  
import requests
from exceptions import ValueError
from time import sleep
import itertools
import networkx as nx  
import matplotlib.pyplot as plt
import community as co
import operator

#def parse(url):
#    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
#    page = requests.get(url,headers=headers)
#    for i in range(20):
#        sleep(3)
#        try:
#            doc = html.fromstring(page.content)
#            XPATH_NAME = '//h1[@id="title"]//text()'
#            XPATH_SALE_PRICE = '//span[contains(@id,"ourprice") or contains(@id,"saleprice")]/text()'
#            XPATH_ORIGINAL_PRICE = '//td[contains(text(),"List Price") or contains(text(),"M.R.P") or contains(text(),"Price")]/following-sibling::td/text()'
#            XPATH_CATEGORY = '//a[@class="a-link-normal a-color-tertiary"]//text()'
#            XPATH_AVAILABILITY = '//div[@id="availability"]//text()'
# 
#            RAW_NAME = doc.xpath(XPATH_NAME)
#            RAW_SALE_PRICE = doc.xpath(XPATH_SALE_PRICE)
#            RAW_CATEGORY = doc.xpath(XPATH_CATEGORY)
#            RAW_ORIGINAL_PRICE = doc.xpath(XPATH_ORIGINAL_PRICE)
#            RAw_AVAILABILITY = doc.xpath(XPATH_AVAILABILITY)
# 
#            NAME = ' '.join(''.join(RAW_NAME).split()) if RAW_NAME else None
#            SALE_PRICE = ' '.join(''.join(RAW_SALE_PRICE).split()).strip() if RAW_SALE_PRICE else None
#            CATEGORY = ' > '.join([i.strip() for i in RAW_CATEGORY]) if RAW_CATEGORY else None
#            ORIGINAL_PRICE = ''.join(RAW_ORIGINAL_PRICE).strip() if RAW_ORIGINAL_PRICE else None
#            AVAILABILITY = ''.join(RAw_AVAILABILITY).strip() if RAw_AVAILABILITY else None
# 
#            if not ORIGINAL_PRICE:
#                ORIGINAL_PRICE = SALE_PRICE
#            #retrying in case of caotcha
#            if not NAME :
#                raise ValueError('captcha')
#
#            data = {
#                    'NAME':NAME,
#                    'SALE_PRICE':SALE_PRICE,
#                    'CATEGORY':CATEGORY,
#                    'ORIGINAL_PRICE':ORIGINAL_PRICE,
#                    'AVAILABILITY':AVAILABILITY,
#                    'URL':url,
#                    }
# 
#            return data
#        except Exception as e:
#            print e


#format param datas : authors_in_paper = [[1,2,3,4,5],[1,8,3],[2,9],[10]]
#return a Network of Authors/Data
def generate_graph_with_edge_list(G, data2D):
       
    for data in data2D:
        #untuk paper yg hanya dibuat oleh author > 1, buat edge list author
        if (len(data)>1):
            #membuat pasangan edge_list dari kombinasi value dalam list data
            edge_list_data = list(itertools.combinations(data,2))
            #menambahkan edge list ke dalam graph
            for edge_list in edge_list_data:
                G.add_edge(edge_list[0],edge_list[1])
                
        #untuk author tunggal tambahkan langsung mjd node pada graph
#        else:      
#            if(len(data)==1): #ada beberapa li entry proceeding formatnya bukan paper dan author jadi pastikan minimal 1.
#                G.add_node(data[0])    
    
       
    return G     
    
def readConference(conflist_id):
    #4D array untuk semua conflist_id
    extracted_data = []
   
    for i in conflist_id:
        url = "http://dblp.uni-trier.de/db/conf/"+i
        print "Scrap-Processing: "+url
        extracted_data.append(parse_dblp_author_in_conference(url))
    
    return extracted_data
       
                                   
def parse_dblp_author_in_conference(url):
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36'}
    page = requests.get(url,headers=headers)
    try:
        doc = html.fromstring(page.content)
        #XPATH_ISBN = '//div[@class="data"]//span[@itemprop="isbn"]//text()'        
        #XPATH_DATE = '//div[@class="data"]//span[@itemprop="datePublished"]//text()'
        XPATH_CONTENT_LINK = '//div[@class="data"]//a/@href'
        
        #isbn = doc.xpath(XPATH_ISBN)       
        #date = doc.xpath(XPATH_DATE)
        conference_link = doc.xpath(XPATH_CONTENT_LINK)
        
        # 3D array author in all conference
        arr_id_authors_per_paper_all_conference = []
        
        for cl in conference_link:
            page = requests.get(cl,headers=headers)
            # 2D array author per paper di conference di tahun tertentu
            arr_id_authors_per_paper_per_conference = []
            try:
                doc = html.fromstring(page.content)
                #get all id paper from li
                XPATH_ID_PAPER_IN_LI = '//li[@class="entry inproceedings"]/@id'
                #untuk setiap id li, baru ambil author2x. simpan di dalam array paper
                #tambahkan ke array yang menampung conference append               
                arr_id_paper = doc.xpath(XPATH_ID_PAPER_IN_LI)
                for id in arr_id_paper:
                    XPATH_AUTHOR_PAPER_LINK = '//li[@id="'+id+'"]//div[@class="data"]//a/@href'
                    authors_per_paper = doc.xpath(XPATH_AUTHOR_PAPER_LINK)
                    #ambil id terakhir pada link person                    
                    arr_id_authors_per_paper = []                    
                    for auth in authors_per_paper:
                        arr_id_authors_per_paper.append(auth.rsplit('/',1)[-1])                            
                                               
                    #tambahkan ke array conference pada tahun tertentu
                    arr_id_authors_per_paper_per_conference.append(arr_id_authors_per_paper)
                #tambahkan ke array all conference   
                arr_id_authors_per_paper_all_conference.append(arr_id_authors_per_paper_per_conference)                
                
            except Exception as e:
                print e
        
        return arr_id_authors_per_paper_all_conference                        
    except Exception as e:
        print e
  
#run louvain algorithm community detection, G = network (sudah ada vertex dan edge)
def run_louvain_cd(G,show_com_list,savefile):
    print "running Louvain Algorithm..."
    part = co.best_partition(G)
    #bikin part baru iterate, yang urutannya sesuai dengan g.nodes￼
    part2 = [] #list baru
    #print list(G)
    for x in G.nodes():
        part2.append(part[x])

    #set color for each community
    part_id = [ float((_x+1)) for _x in part2]
    colors = [ (_i/(_i+3)) for _i in part_id]
        
    #draw graph and apply the colors for each community.
    nx.draw_networkx(G,node_color = colors,  with_labels=False, font_size=8, alpha=0.5, node_size=18 )

    print "========================================================================="
    print "Network Descriptions"
    print "========================================================================="    
    print "Modularity: ", co.modularity(part,G)
    print "Num. of Vertices:", G.number_of_nodes()
    print "Num. of Edges: ", G.number_of_edges()
    print "Network Size:", G.size()   
    print "========================================================================="
    print "Detected Communities Based On Louvain Algorithm(Member , Community ID)"
    print "Number of Communities Detected:",  len(set(part.values()))    
    print "=========================================================================\n"    
    
    sorted_part = sorted(part.items(),key=operator.itemgetter(1))
    
    if savefile == True:
        f = open('com_list_louvain','wb')
        f.write("community_detected using Louvain Algorithm: (member : id community) \n" )
        for val in sorted_part:
            f.write("%s \n" % str(val))        
        f.close()
        
    if show_com_list == True:
        print "Community List : \n" 
        print  sorted_part
    
    plt.show()

#menyimpan graph dalam format edgelist (original f1 dan converted f2, f3 mapping id)
def generate_edgelistfile(G): 
    print "Creating dblp_nodes_id file..."
    f3=open('dblp_nodes_id','wb')
    dict_id_authors = {}
    #print G.nodes
    for key,val in zip(G.nodes,range(len(G.nodes))):
        dict_id_authors[key]=val
        f3.write("%s : %d \n" % (key, val+1))
    f3.close()
    
    print "Creating dblp_data and edgelist file..."
    #print dict_id_authors['Andrade:Ewerton_R=']+1 = 336 (eurosp)
    f1=open('dblp_data','wb')
    f2=open('dblp_edgelist','wb')    
    
    for u,v in sorted(G.edges()):
        f1.write("%s %s\n" % (u, v))
        #convert tiap nama ke integer mulai dari 1 biar bisa dibaca di LEMON
        f2.write("%d %d\n" % (dict_id_authors[u]+1,dict_id_authors[v]+1) )
        
    f1.close()
    f2.close()
    
################## ENTRY POINT #################################
if __name__ == "__main__":
      
    #1. siapkan array link id conference yang ingin di scrap authornya per paper
    conflist_id = ['sp', 'eurosp', 'cvpr'] # sp, eurosp, cvpr, issi, 
    
    #2. lakukan scrapping authors , return array 4D
    extracted_data = readConference(conflist_id)

    #3. siapkan Graph kosong
    G = nx.Graph()

    #4. membuat edge list pada Graph berdasarkan data (2D array:lihat generate_graph_with_edge_list) hasil scrapping
    for data in extracted_data:
       #3D Array conference  
       for conf in data:
           generate_graph_with_edge_list(G,conf)
        
    #5. (optional) save ke file edgelist    id dimulai dari 1
    generate_edgelistfile(G)
        
    #4. Jalankan algoritma Louvain Community Detection
    run_louvain_cd(G,show_com_list=False, savefile = True)