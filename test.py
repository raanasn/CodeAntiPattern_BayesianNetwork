#teste [barname, [features], cross[5,7,10], percent[0.1-0.9]] wa dar biar chi delete
#BENEWIS

#loge taki
#learning percent?(aya be tanhayi nabayad ru jek f?)

#Akhar sar bad smell ezafe


import os, time
from fit_data import test_data
#!!!!!!!!!crossed_arr and len_bs -> Hand

#(len f, percent, accuracy, [] f, data, split sheet)
#name (9)1-9   0.  weighted-macro-micro [0-8]  smells/equal/none cross  sheet

'''for p in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    test_data("_jgraph",9,p, None, [],"equal",5,"Sheet1")

for n in [1,2,3,4,5,6,7,8,9]:
    test_data("_jgraph",n,0.5, None, [],"equal",5,"Sheet2")'''

for arr in [[0],[1],[2],[3],[4],[5],[6],[7],[8]]:
    test_data("_jgraph",9,0.5, None, arr,"equal",5,"Sheet3")

#array([recall0,recall1]) array([precision0,precision1]) (ba inke baraks chap shode)
os.system('mpg123 Input/fuehlen.mp3')

