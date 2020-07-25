#teste [barname, [features], cross[5,7,10], percent[0.1-0.9]] wa dar biar chi delete

import os, time
from output import *
from fit_data import test_data
#!!!!!!!!!crossed_arr and len_bs -> Hand

#(len f, percent, accuracy, [] f, data, split sheet structure)
#name (9)1-9   0.  weighted-macro-micro [0-8]  smells/equal/none cross  sheet parent/child/both

'''for n in [1, 2, 3, 4, 5, 6, 7, 8]:
    test_data("_freemind_new", n, 0.9, None, [], "equal", 5, "Sheet1", "parent")

for arr in [[0], [1], [2], [3], [4], [5], [6], [7]]:
    test_data("_freemind_new", 8, 0.9, None, arr, "equal", 5, "Sheet2", "parent")

for n in [1, 2, 3, 4, 5, 6, 7, 8]:
    test_data("_freemind_new", n, 0.6, None, [], "equal", 5, "Sheet3", "parent")

for arr in [[0], [1], [2], [3], [4], [5], [6], [7]]:
    test_data("_freemind_new", 8, 0.6, None, arr, "equal", 5, "Sheet4", "parent")

for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    test_data("_freemind_new", 8, p, None, [0], "equal", 5, "Sheet5", "parent")

color("_freemind_new",5)

for n in [1, 2, 3, 4, 5, 6, 7, 8]:
    test_data("_jedit", n, 0.8, None, [], "equal", 5, "Sheet1", "parent")

for arr in [[0], [1], [2], [3], [4], [5], [6], [7]]:
    test_data("_jedit", 8, 0.8, None, arr, "equal", 5, "Sheet2", "parent")

for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    test_data("_jedit", 6, p, None, [], "equal", 5, "Sheet3", "parent")

for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    test_data("_jedit", 8, p, None, [6], "equal", 5, "Sheet4", "parent")

color("_jedit", 4)

for p in [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]:
    test_data("_argo", 6, p, None, [], "equal", 5, "Sheet1", "parent")

for n in [1, 2, 3, 4, 5, 6, 7, 8]:
    test_data("_argo", n, 0.9, None, [], "equal", 5, "Sheet2", "parent")

for arr in [[0], [1], [2], [3], [4], [5], [6], [7]]:
    test_data("_argo", 8, 0.9, None, arr, "equal", 5, "Sheet3", "parent")

for n in [1, 2, 3, 4, 5, 6, 7, 8]:
    test_data("_argo", n, 0.2, None, [], "equal", 5, "Sheet4", "parent")

for arr in [[0], [1], [2], [3], [4], [5], [6], [7]]:
    test_data("_argo", 8, 0.2, None, arr, "equal", 5, "Sheet5", "parent")

color("_argo", 5)'''



#array([recall0,recall1]) array([precision0,precision1]) (ba inke baraks chap shode)
os.system('mpg123 Input/fuehlen.mp3')

