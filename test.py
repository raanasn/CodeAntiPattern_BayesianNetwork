# mishe marze predict ro taghir dad?
# train bar asas mix f1, f1 o f2,
# barname be barname
# hame barname ha
# Akhar sar bad smell ezafe

import os, time
from fit_data import test_data

#(len f, percent, accuracy, [] f, data)
# (0)1-9   0.  weighted-macro-micro [0-8]  smells/equal/none
res=test_data(9, 0.25, None, [],"equal")
print(res)
res=test_data(9, 0.50, None, [],"equal")
print(res)
res=test_data(9, 0.60, None, [],"equal")
print(res)
res=test_data(9, 0.70, None, [],"equal")
print(res)

#recall/precision
#array([,specifity(0)]) array([,sensitivity(1)])
os.system('mpg123 Input/fuehlen.mp3')

