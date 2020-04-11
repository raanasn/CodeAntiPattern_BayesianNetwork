# mishe marze predict ro taghir dad?
# train bar asas mix f1, f1 o f2,
# barname be barname
# hame barname ha
# Akhar sar bad smell ezafe

import os, time
from fit_data import test_data

res=[]
try:
    #aval ino motmaen sho eyne ham
    res.append(test_data(0, 0.7, "weighted", 0))
    print(res)
except:
    os.system('mpg123 Input/fuehlen.mp3')
os.system('mpg123 Input/ham.mp3')