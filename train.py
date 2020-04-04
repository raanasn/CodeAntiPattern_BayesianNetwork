#in wa 9 o 10
#test shabake-bia baze dorost kon wa ran kon

#baad chand barname
#baad bad smell ezafe

from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import pickle
import itertools


name="_freemind"
class_objects = pickle.load(open("classes"+name+".pkl", "rb"))

model = BayesianModel()
for i in range(1,4):#badsmell
   for j in range(1,4):#feature
      model.add_edge('b'+str(i),'f'+str(j)+'_p')
      model.add_edge('b' + str(i), 'f' + str(j) + '_c')

all_features=[]
all_smells=[]
for class_ in class_objects:
   kasr=0
   zarib=[]
   f=[]
   for parent in class_.parents:
      kasr=parent[1].weight + kasr #bayad ye dor kamel bere
      zarib.append(parent[1].weight)
   for i in range(0,3):#feature
      foo=0
      for p,z in zip(class_.parents,zarib):
         foo=(p[0].features[i]*z/kasr)+foo
      f.append(foo)
   all_features.append(f)
   all_smells.append(class_.features[9])

max = [max(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
min = [min(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]

cpds=[]
for f,b in zip(all_features,all_smells):
   for i in range(3):#features
      high=0
      low=0
      if  f[i]>=(max[i]*0.5):
         high=high+1
      else:
         low=low+1
      cpds.append(TabularCPD('f_'+str(i), 2, [[high], [low]]))
'''for i in range(0,3):
   max_=max(c.features[i] for c in class_objects)
   min_=min(c.features[i] for c in class_objects)
   diff=max_-min_
   high, med_h, med_l,low=0
   for c in class_objects:
      if c.features[i]>=diff*0.5:
         high=high+1
      else:
         low=low+1
   elif c.features[i]>diff*0.5:
           med_h=med_h+1
      elif c.features[i]>diff*0.25:
           med_l=med_l+1
   cpds.append([high,low])'''

#cpd_b1 = TabularCPD('b1', 2, [[0.4], [0.6]])#WTF