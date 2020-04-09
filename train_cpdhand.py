from pgmpy.models import BayesianModel
from pgmpy.factors.discrete import TabularCPD
import pickle
import numpy as np
import itertools

name="_freemind"
class_objects = pickle.load(open("classes"+name+".pkl", "rb"))

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
diff= [(i-j)*0.5 for i,j in zip(max,min)]

# 0 T T T
# 1 T T F
# 2 T F T
# 3 T F F
# 4 F T T
# 5 F T F
# 6 F F T
# 7 F F F

table_true=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]] #smells
table_false=[[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0]]

table_high=[0,0,0]#features
table_low=[0,0,0]
for f,b in zip(all_features,all_smells):
   for i in range(3):#smells
      if f[0]>=diff[0]:
         table_high[0]=table_high[0]+1
         if f[1]>=diff[1]:
            table_high[1] = table_high[1] + 1
            if f[2]>=diff[2]:
               table_high[2] = table_high[2] + 1
               table_true[i][0]=table_true[i][0]+b[i]
               table_false[i][0] = table_false[i][0] + (b[i]-1)*(-1)
            else:
               table_low[2] = table_low[2] + 1
               table_true[i][1]=table_true[i][1]+b[i]
               table_false[i][1] = table_false[i][1] + (b[i] - 1) * (-1)
         else:
            table_low[1] = table_low[1] + 1
            if f[2]>=diff[2]:
               table_high[2] = table_high[2] + 1
               table_true[i][2]=table_true[i][2]+b[i]
               table_false[i][2] = table_false[i][2] + (b[i] - 1) * (-1)
            else:
               table_low[2] = table_low[2] + 1
               table_true[i][3]=table_true[i][3]+b[i]
               table_false[i][3] = table_false[i][3] + (b[i] - 1) * (-1)
      else:
         table_low[0] = table_low[0] + 1
         if f[1]>=diff[1]:
            table_high[1] = table_high[1] + 1
            if f[2]>=diff[2]:
               table_high[2] = table_high[2] + 1
               table_true[i][4]=table_true[i][4]+b[i]
               table_false[i][4] = table_false[i][4] + (b[i] - 1) * (-1)
            else:
               table_low[2] = table_low[2] + 1
               table_true[i][5]=table_true[i][5]+b[i]
               table_false[i][5] = table_false[i][5] + (b[i] - 1) * (-1)
         else:
            table_low[1] = table_low[1] + 1
            if f[2]>=diff[2]:
               table_high[2] = table_high[2] + 1
               table_true[i][6]=table_true[i][6]+b[i]
               table_false[i][6] = table_false[i][6] + (b[i] - 1) * (-1)
            else:
               table_low[2] = table_low[2] + 1
               table_true[i][7]=table_true[i][7]+b[i]
               table_false[i][7] = table_false[i][7] + (b[i] - 1) * (-1)

#between 0 and 1
len_=len(class_objects)
table_high[:] = [x / (3*len_) for x in table_high]
table_low[:] = [x / (3*len_) for x in table_low]
table_t=(np.array(table_true)/len_).tolist()
table_f =(np.array(table_false)/len_).tolist()

model = BayesianModel()
for i in range(1, 4):  # badsmell
   for j in range(1, 4):  # feature
      model.add_edge('f' + str(j), 'b' + str(i))

cpds=[]
for i in range(3): #features
   model.add_cpds(TabularCPD('f'+str(i+1), 2, [[table_high[i]], [table_low[i]]]))
print(table_t[0],table_f[0])
for i in range(3): #smells
   model.add_cpds(TabularCPD(
         'b'+str(i+1), 2,
         [table_t[i], table_f[i]],
         evidence=['f1', 'f2','f3'],
         evidence_card=[2, 2, 2])
         )
print(model.get_cpds())
print(model.edges())
print(model.check_model())