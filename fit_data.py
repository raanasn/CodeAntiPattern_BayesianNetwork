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
len_f=3
len_bs=3

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


values = pd.DataFrame(data={'f1': features[0], 'f2': features[1], 'f3': features[2],
                          'b1': all_smells[0],'b2': all_smells[1], 'b3': all_smells[2]})

model = BayesianModel()
for i in range(1, len_bs+1):  # badsmell
   for j in range(1, len_f+1):  # feature
      model.add_edge('f' + str(j), 'b' + str(i))

train_data = values[:350]
test_data  = values[350:]
predict_data = test_data.copy()
predict_data.drop(['b1','b2','b3'], axis=1, inplace=True)
test_data.drop(['f1','f2','f3'], axis=1, inplace=True)
model.fit(train_data)
y_pred = model.predict(predict_data)

print("Acc: ",accuracy_score(test_data,y_pred))
print("Precision: ",precision_score(test_data,y_pred,average=None))
print("Recall: ",recall_score(test_data,y_pred,average=None))


