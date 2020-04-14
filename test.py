# mishe marze predict ro taghir dad?
# train bar asas mix f1, f1 o f2,
# barname be barname
# hame barname ha
# Akhar sar bad smell ezafe

import os, time
from fit_data import test_data

res=[]

#(len f, percent, accuracy, one f, data)
# (0)1-9   0.  weighted-macro-micro 0-8 all-smells-equal
res.append(test_data(1, 0.7, "weighted", 0,"smells"))
res.append(test_data(1, 0.5, "weighted", 0,"smells"))
res.append(test_data(2, 0.7, "weighted", 0,"smells"))
res.append(test_data(2, 0.5, "weighted", 0,"smells"))
res.append(test_data(3, 0.7, "weighted", 0,"smells"))
res.append(test_data(3, 0.5, "weighted", 0,"smells"))
res.append(test_data(4, 0.7, "weighted", 0,"smells"))
res.append(test_data(4, 0.5, "weighted", 0,"smells"))
res.append(test_data(5, 0.7, "weighted", 0,"smells"))
res.append(test_data(5, 0.5, "weighted", 0,"smells"))
res.append(test_data(6, 0.7, "weighted", 0,"smells"))
res.append(test_data(6, 0.5, "weighted", 0,"smells"))
res.append(test_data(7, 0.7, "weighted", 0,"smells"))
res.append(test_data(7, 0.5, "weighted", 0,"smells"))
res.append(test_data(8, 0.7, "weighted", 0,"smells"))
res.append(test_data(8, 0.5, "weighted", 0,"smells"))
print(res)
os.system('mpg123 Input/fuehlen.mp3')

