#teste [barname, [features], cross[5,7,10], percent[0.1-0.9]] wa dar biar chi delete



import os, time
from output import *
from fit_data import test_data
#!!!!!!!!!crossed_arr and len_bs -> Hand

#(len f, percent, accuracy, [] f, data, split sheet structure)
#name (9)1-9   0.  weighted-macro-micro [0-8]  smells/equal/none cross  sheet parent/child

for n in [1,2,3,4,5,6,7,8,9]:
    test_data("_freemind",n,0.5, None, [],"equal",5,"Sheet1","child")

for arr in [[0],[1],[2],[3],[4],[5],[6],[7],[8]]:
    test_data("_freemind",9,0.5, None, arr,"equal",5,"Sheet2","child")

for p in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    test_data("_freemind",9,p, None, [],"equal",5,"Sheet3","child")

color("_freemind",3)

for n in [1,2,3,4,5,6,7,8,9]:
    test_data("_jgraph",n,0.5, None, [],"equal",5,"Sheet1","child")

for arr in [[0],[1],[2],[3],[4],[5],[6],[7],[8]]:
    test_data("_jgraph",9,0.5, None, arr,"equal",5,"Sheet2","child")

for p in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    test_data("_jgraph",9,p, None, [],"equal",5,"Sheet3","child")

color("_jgraph",3)

for n in [1,2,3,4,5,6,7,8,9]:
    test_data("_junit",n,0.5, None, [],"equal",5,"Sheet1","child")

for arr in [[0],[1],[2],[3],[4],[5],[6],[7],[8]]:
    test_data("_junit",9,0.5, None, arr,"equal",5,"Sheet2","child")

for p in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    test_data("_junit",9,p, None, [],"equal",5,"Sheet3","child")

color("_junit",3)

for n in [1,2,3,4,5,6,7,8,9]:
    test_data("_jag",n,0.5, None, [],"equal",5,"Sheet1","child")

for arr in [[0],[1],[2],[3],[4],[5],[6],[7],[8]]:
    test_data("_jag",9,0.5, None, arr,"equal",5,"Sheet2","child")

for p in [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9]:
    test_data("_jag",9,p, None, [],"equal",5,"Sheet3","child")

color("_jag",3)

#array([recall0,recall1]) array([precision0,precision1]) (ba inke baraks chap shode)
os.system('mpg123 Input/fuehlen.mp3')

