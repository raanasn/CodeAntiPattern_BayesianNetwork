import itertools
import pandas as pd
import numpy as np
from pgmpy.models import BayesianModel
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import pickle

def shuffle(df, n=1, axis=0):
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df

def model(features,all_smells,properties,len_bs,len_f,f_number,accuracy,diff_precent):
    if properties=="equal":
        values = pd.DataFrame(data={'b': all_smells})
    else:
        values=pd.DataFrame(data={'b0': all_smells[0],'b1': all_smells[1],'b2':all_smells[2]})

    if f_number!=[]:
        for i,j in zip(f_number,range(len(features))):
            d = pd.DataFrame({'f' + str(i): features[j]})
            values = pd.concat([values, d], axis=1)
    else:
        for i in range(len_f):
            d=pd.DataFrame({'f'+str(i):features[i]})
            values = pd.concat([values, d], axis=1)

    model = BayesianModel()
    if f_number!=[]:
        for i in range(len_bs):
            for j in f_number:
                model.add_edge('f' + str(j), 'b' + str(i))
    elif properties!="equal":
        for i in range(len_bs):  # badsmell
            for j in range(len_f):  # feature
                model.add_edge('f' + str(j), 'b'+str(i))
    elif properties=="equal":
        for j in range(len_f):  # feature
            model.add_edge('f' + str(j), 'b')

    values=shuffle(values)
    train_data = values[:int((len(all_smells)*0.7))]
    test_data  = values[int((len(all_smells)*0.7)):]
    predict_data = test_data.copy()

    delete=[]
    for f in range(len_f):
        if (train_data['f'+str(f)] == 0).all():
            delete.append(f)
    for item in delete:
        del train_data['f'+str(item)]
        del predict_data['f' + str(item)]
        model.remove_node('f'+str(item))

    if f_number!=[]:
        predict_data.drop(['b0', 'b1', 'b2'], axis=1, inplace=True)
        for i in f_number:
            test_data.drop(['f' + str(i)], axis=1, inplace=True)
    elif properties!="equal":
        predict_data.drop(['b0','b1','b2'], axis=1, inplace=True)
        for i in range(len_f):
            test_data.drop(['f' + str(i)], axis=1, inplace=True)
    elif properties=="equal":
        predict_data.drop(['b'], axis=1, inplace=True)
        for i in range(len_f):
            test_data.drop(['f' + str(i)], axis=1, inplace=True)

    model.fit(train_data)

    y_pred = model.predict(predict_data)
    precent_pred=model.predict_probability(predict_data)
    res=[]

    if properties=="equal":
        res.append(str(len_f) + " " + str(f_number) + " " + str(accuracy) + " " + str(diff_precent) + " " + "b")
        res.append(accuracy_score(test_data['b'], y_pred['b']))
        res.append(precision_score(test_data['b'], y_pred['b'], average=accuracy))
        res.append(recall_score(test_data['b'], y_pred['b'], average=accuracy))
        '''print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        for ((index, row),(index2,row2)) in zip(test_data.iterrows(), y_pred.iterrows()):
            print(row['b'],row2['b'])
            print("***********")'''
        return res
    for i in range(len_bs):
        res.append([])
        res[i].append(str(len_f)+" "+str(f_number)+" "+str(accuracy)+" "+str(diff_precent)+" "+"b"+str(i))
        res[i].append(accuracy_score(test_data['b'+str(i)],y_pred['b'+str(i)]))
        res[i].append(precision_score(test_data['b'+str(i)],y_pred['b'+str(i)],average=accuracy))
        res[i].append(recall_score(test_data['b'+str(i)],y_pred['b'+str(i)],average=accuracy))
    return res



def test_data(len_f,diff_precent,accuracy,f_number,properties):#len_f=special range, f_number=special f

    #feature set is devided by hand
    #f_len is in the first loop written with hand (9)
    #len_bs is just in the model written with hand
    len_bs = 3

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
       if properties=="smells":
           flag=False
           for s in range(len_bs):
               if class_.features[9][s]==1:
                   flag=True
           if flag==False:
               continue
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

    sum_=[sum(i) for i in all_smells]
    equal_features = []
    equal_smells=[]
    for item in all_smells:
        equal_smells.append(item)
    if properties=="equal":
        delete=[]
        for item in range(len_bs):
            delete.append([])
        for bs in range(len_bs):
            count=0
            for i in range(len(all_smells[0])):
                if count>sum_[bs] and all_smells[bs][i]==0:
                    delete[bs].append(i)
                elif all_smells[bs][i]==0:
                    count+=1
        for d,fi,b in zip(delete,range(len_bs),equal_smells):
            feat=all_features.copy()
            for item in reversed(d):
                del feat[item]
                del b[item]
            equal_features.append(feat)

    max_=[]
    min_=[]
    diff=[]
    if properties=="equal":
        for item in equal_features:
            ma = [max(i) for i in itertools.zip_longest(*item, fillvalue = 0)]
            mi = [min(i) for i in itertools.zip_longest(*item, fillvalue = 0)]
            dif= [(i-j)*diff_precent for i,j in zip(ma,mi)]
            max_.append(ma)
            min_.append(mi)
            diff.append(dif)
    else:
        max_ = [max(i) for i in itertools.zip_longest(*all_features, fillvalue=0)]
        min_ = [min(i) for i in itertools.zip_longest(*all_features, fillvalue=0)]
        diff = [(i - j) * diff_precent for i, j in zip(max_, min_)]

    features=[]
    equal_f = []
    res = []

    if f_number!=[]:
        for i in range(len(f_number)):
            features.append([])
        arr=len(features)
        for f in all_features:
            for fn,ar in zip(f_number,range(arr)):
                if f[fn] >= diff[fn]:
                    features[ar].append(1)
                else:
                    features[ar].append(0)
        res = model(features, all_smells, properties, len_bs, len_f, f_number, accuracy, diff_precent)
        return res
    elif properties != "equal":
        for i in range(len_f):
            features.append([])
        for f in all_features:
            for i in range(len_f):
                if f[i] >= diff[i]:
                    features[i].append(1)
                else:
                    features[i].append(0)
        res=model(features,all_smells,properties,len_bs,len_f,f_number,accuracy,diff_precent)
        return res
    elif properties == "equal":
        for i in range(len_f):
            features.append([])
        for fb,bs in zip(equal_features,range(len_bs)):
            for fea in fb:
                for i in range(len_f):
                    if fea[i] >= diff[bs][i]:
                        features[i].append(1)
                    else:
                        features[i].append(0)
            equal_f.append(features.copy())
            for i in range(len_f):
                features[i]=[]

        res.append(model(equal_f[0], equal_smells[0], properties, len_bs, len_f, f_number, accuracy, diff_precent))
        res.append(model(equal_f[1], equal_smells[1], properties, len_bs, len_f, f_number, accuracy, diff_precent))
        res.append(model(equal_f[2], equal_smells[2], properties, len_bs, len_f, f_number, accuracy, diff_precent))
        return res
