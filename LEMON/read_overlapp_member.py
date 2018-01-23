import networkx as nx  
import matplotlib.pyplot as plt
import community as co
import numpy as np
#import matplotlib.cm as cm
 
def generate_overlapp_vertex_file():
    with open('output_lemon', 'U') as f:
        #hanya temporary saja    
        temp = set ()
        #untuk nampung vertex2x yg overlap
        overlap_member = set ()     
        total_vertex = 0
        #baca tiap baris
        i = 0 
        for line in f.readlines():
            if not line.strip().startswith("#"):
                #split baris berdasarkan koma, masukkan dalam set
                line = line.replace(" ", "")
                #print line
                set_member = set(line.strip().split(','))
                #print i                
                print "set-member : " , len(set_member)
                #print "set : ke ", set_member
                total_vertex += len(set_member)
                #print total_vertex
                if (len(temp.intersection(set_member)) == 0  ):
                    temp = temp.union(set_member) 
                else:
                    old = temp
                    #print "old : ", old
                    temp = temp.intersection(set_member)
                    #print "temp intersection : ", temp
                    overlap_member = overlap_member.union(temp)
                    #print "overlap_member : ", overlap_member
                    temp = temp.union(old, set_member)       
                    #print "temp : ", temp
            i +=1
            
    print "Total Vertex Overlap : ", len(overlap_member)
    print "Total Vertex hasil union (unique) :", len(temp)
    print "total Vertex dari semuanya : ", total_vertex    
    #print "Rataan vertex perkomunitas: ", total_vertex/38
    f = open('overlapp_member_community','wb')
    for member in list(overlap_member): 
        #print member
        member = str(member).replace(" ","")        
        f.write(member) 
        f.write("\n")
    f.close()
    print "Finish write overlap communities."
    
################## ENTRY POINT #################################
if __name__ == "__main__":
    #1. output overlapp_member_community
    generate_overlapp_vertex_file()
    #2. 
    G = nx.Graph()    
    G_lemons = nx.Graph()
    
    with open('../f2_edgelist_map_id','U') as f:
        for line in f.readlines():
            line = line.strip().split(' ')
            #print line
            G.add_edge(line[0],line[1])
    
    com_lemon = []
    with open('output_lemon_dblp','U') as f:
        for line in f.readlines():
            if not line.strip().startswith("#"):
                #split baris berdasarkan koma, masukkan dalam set
                line = line.strip().split(',')  
                line = [x.strip(' ') for x in line]
                #print line
                com_lemon.append (line)
    
    #Siapkan Warna
    col = ['c','r','g','b','k','y','#663d00','#e68a00', '#00ffff','#8cff1a','#660066','#663300','#996600','#999966','#99cc00','#ccccff','#00ff99','#669999','#cc0066','#660033','#ff33cc','#006600','#ffffff','#333300','#ccff66','#ffcc99','#003300','#009933','#ff0066','#cc0000','#993333','#66ff66','#003366','#336699','#333300','#3366ff','#000099','#33cccc','#ff9999']
    
    #substract graph berdasarkan hasil komunitas lemon : output_lemon_dblp
    g = nx.Graph()
    i = 1 

    for com in com_lemon:
        print "....buildcommunity : ", i
        g = G.subgraph(com)
        for node in g.nodes():
            g.node[node]['color'] = col[i-1]
            #print node, i-1
        G_lemons = nx.compose(G_lemons,g)
        #print G_lemons.nodes()
        i +=1
#        if i == 3 :
#            break
    
    #Tulis ke file buat di gephi
    nx.write_gexf(G_lemons,"co-author.gexf")    
    
    
    overlapmember = []
    # Ubah warna yang overlapp member community
    with open('overlapp_member_community','U') as f:
        for line in f.readlines():
            line = line.strip('\n')
            s = str(line)
            overlapmember.append(s)
    
    if (len(overlapmember) != 0) :        
            #Setting Tampilan vertex yang overlap
            for node in G_lemons.nodes:
                for o in overlapmember:      
                    if node == o :
                        G_lemons.node[node]['color'] = '#ff1aff'  
                        G_lemons.node[node]['size'] = 100
                        G_lemons.node[node]['label'] = node
                        break
                    else:
                        #G_lemons.node[node]['color'] = 'r' 
                        G_lemons.node[node]['size'] = 15
                        G_lemons.node[node]['label'] = ''
            
            color_map = []
            size_map = []
            labels = {}
            for node in G_lemons.nodes:
                color_map.append(G_lemons.node[node]['color'])
                size_map.append(G_lemons.node[node]['size'])
                labels[node] = G_lemons.node[node]['label']
           
            pos = nx.spring_layout(G_lemons)
            plt.figure("Lemons Communities")
            plt.rcParams['axes.facecolor'] = '#ffffb3'
            nx.draw_networkx(G_lemons, pos, node_color = color_map, labels = labels, node_size = size_map, with_labels = True, width = 0.1, alpha = 0.4,font_size=8) 
            
            plt.show()
            
        #    part = co.best_partition(G_lemons)   
        #    print "Number of Communities Detected:",  len(set(part.values()))
        #    print "Modularity: ", co.modularity(part,G_lemons)
        #    
        #    part = co.best_partition(G)
        #    print "Modularity: ", co.modularity(part,G_lemons)        
                
        
        
        
        
        