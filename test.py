import os, time
from fit_data import test_data

print(test_data(9,0.7,"weighted"))
print(test_data(9,0.65,"weighted"))
print(test_data(9,0.5,"weighted"))
print(test_data(9,0.25,"weighted"))

os.system('mpg123 Input/ham.mp3')