# mishe marze predict ro taghir dad / marze diff
# idee: train ru faghat unhayi ke daran ya mosavi
#       train barname be barname
#       train hame barname
#       train bar asas f1, f1 o f2, ..
# Akhar sar bad smell ezafe

import itertools
import pandas as pd
from pgmpy.models import BayesianModel
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import pickle


#initialization
len_f=1 #and first loop had to
len_bs=3
diff_precent=0.7

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
   for i in range(9):#only this one
      foo=0
      for p,z in zip(class_.parents,zarib):
         foo=(p[0].features[i]*z/kasr)+foo
      f.append(foo)
   if class_.features[8] == 1:#cycle (its his issue not his parents)
       f[8]=1
   all_features.append(f)
   for bs in range(len_bs):
        all_smells[bs].append(class_.features[9][bs])

max = [max(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
min = [min(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
diff= [(i-j)*diff_precent for i,j in zip(max,min)]

features=[]
for i in range(len_f):
    features.append([])

for f in all_features:
    for i in range(len_f):
        if f[i] >= diff[i]:
            features[i].append(1)
        else:
            features[i].append(0)

values=pd.DataFrame(data={'b0': all_smells[0],'b1': all_smells[1], 'b2': all_smells[2]})
for i in range(len_f):
    d=pd.DataFrame({'f'+str(i):features[i]})
    values = pd.concat([values, d], axis=1)

model = BayesianModel()
for i in range(len_bs):  # badsmell
   for j in range(len_f):  # feature
      model.add_edge('f' + str(j), 'b' + str(i))

train_data = values[:350]
test_data  = values[350:]
predict_data = test_data.copy()
predict_data.drop(['b0','b1','b2'], axis=1, inplace=True)
for i in range(len_f):
    test_data.drop(['f'+str(i)],axis=1,inplace=True)
model.fit(train_data)

y_pred = model.predict(predict_data)
precent_pred=model.predict_probability(predict_data)

print("Acc: ",accuracy_score(test_data,y_pred))
print("Precision: ",precision_score(test_data,y_pred,average=None))
print("Recall: ",recall_score(test_data,y_pred,average=None))

'''for i in range(350,len(y_pred)+350):
    print(test_data.loc[[i]])
    print(y_pred.loc[[i]])
    print(precent_pred.loc[[i]])
    print("***********")'''

import os, time

os.system('mpg123 Input/ham.mp3')