# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 13:07:47 2018

@author: nano
"""

import json
import gzip
   
#def parse(path): 
#    g = gzip.open(path, 'r') 
#    for l in g: 
#        yield eval(l)
        
def parse(path): 
    g = gzip.open(path, 'r') 
    for l in g: 
        yield json.dumps(eval(l))

f_pengguna = open("amz_pengguna.csv", 'w') 
f_produk   = open("amz_produk.csv", 'w')

i = 0
dict_data = []
for l in parse("reviews_Kindle_Store_5.json.gz"): 
    if i<200:
        data = json.loads(l)
        f_pengguna.write(data["reviewerID"]) 
        f_pengguna.write(",")
        f_pengguna.write(data["reviewerName"])
        f_pengguna.write("\n")
        #print data
        dict_data.append(data)
    else:
        break
    i +=1
    
f_pengguna.close()

'''
pengguna.csv
======
reviewerID, reviewerName (ada tanda kutipnya), asin (buat hubungin pengguna ke produk)
======
produk.csv
========
asin (idproduk)
========

relasi.csv
==============

=============

'''

#data = parse("reviews_Kindle_Store_5.json.gz")
#print data["overall"]