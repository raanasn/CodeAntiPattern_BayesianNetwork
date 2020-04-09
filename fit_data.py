import pickle
import itertools
import pandas as pd
from pgmpy.models import BayesianModel


#initialization
len_f=0
len_bs=0

#Reading Data
name="_freemind"
class_objects = pickle.load(open("classes"+name+".pkl", "rb"))

#Making data ready for Panda
all_features=[]
all_smells=[[],[],[]]
for class_ in class_objects:
   kasr=0
   zarib=[]
   f=[]
   for parent in class_.parents:
      kasr=parent[1].weight + kasr #has to go one round alone
      zarib.append(parent[1].weight)
   for i in range(len_f):
      foo=0
      for p,z in zip(class_.parents,zarib):
         foo=(p[0].features[i]*z/kasr)+foo
      f.append(foo)
   all_features.append(f)
   for bs in range(len_bs):
        all_smells[bs].append(class_.features[9][bs])

max = [max(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
min = [min(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
diff= [(i-j)*0.5 for i,j in zip(max,min)]

features=[[],[],[]]
for f in all_features:
    for i in range(len_f):
        if f[i] >= diff[i]:
            features[i].append(1)
        else:
            features[i].append(0)


data = pd.DataFrame(data={'f1': features[0], 'f2': features[1], 'f3': features[2],
                          'b1': all_smells[0],'b2': all_smells[1], 'b3': all_smells[2]})

model = BayesianModel()
for i in range(1, len_bs):  # badsmell
   for j in range(1, len_f):  # feature
      model.add_edge('f' + str(j), 'b' + str(i))

model.fit(data)
model.get_cpds()

print(model.get_cpds())
print(model.edges())
print(model.check_model())