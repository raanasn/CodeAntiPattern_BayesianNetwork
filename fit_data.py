import itertools
import pandas as pd
from pgmpy.models import BayesianModel
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score
import pickle

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
####
    sum_=[sum(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
    if properties=="equal":
        delete=[]
        for item in len_bs:
            delete.append([])
        for bs in range(len_bs):
            count=0
            for i in range(all_smells):
                if count>sum[bs]:
                    delete[bs].append(i)
                if all_smells[i][bs]==0:
                    count+=1
        #baadeshdelete
###

    max_ = [max(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
    min_ = [min(i) for i in itertools.zip_longest(*all_features, fillvalue = 0)]
    diff= [(i-j)*diff_precent for i,j in zip(max_,min_)]

    features=[]
    for i in range(len_f):
        features.append([])

    for f in all_features:
        for i in range(len_f):
            if f[i] >= diff[i]:
                features[i].append(1)
            else:
                features[i].append(0)

    if len_f == 0:
        for i in range(len(f_number)):
            features.append([])
        arr=len(features)
        for f in all_features:
            for fn,ar in zip(f_number,range(arr)):
                if f[fn] >= diff[fn]:
                    features[ar].append(1)
                else:
                    features[ar].append(0)


    values=pd.DataFrame(data={'b0': all_smells[0],'b1': all_smells[1],'b2':all_smells[2]})
    for i in range(len_f):
        d=pd.DataFrame({'f'+str(i):features[i]})
        values = pd.concat([values, d], axis=1)

    if len_f==0:
        for i,j in zip(f_number,range(len(features))):
            d = pd.DataFrame({'f' + str(i): features[j]})
            values = pd.concat([values, d], axis=1)

    model = BayesianModel()
    for i in range(len_bs):  # badsmell
        for j in range(len_f):  # feature
            model.add_edge('f' + str(j), 'b'+str(i))

    if len_f==0:
        for i in range(len_bs):
            for j in f_number:
                model.add_edge('f' + str(j), 'b' + str(i))

    train_data = values[:350]
    test_data  = values[350:]
    predict_data = test_data.copy()
    predict_data.drop(['b0','b1','b2'], axis=1, inplace=True)
    for i in range(len_f):
        test_data.drop(['f'+str(i)],axis=1,inplace=True)
    if len_f == 0:
        for i in f_number:
            test_data.drop(['f' + str(i)], axis=1, inplace=True)

    model.fit(train_data)

    y_pred = model.predict(predict_data)
    precent_pred=model.predict_probability(predict_data)
    res=[]

    for i in range(len_bs):
        res.append([])
        res[i].append(str(len_f)+" "+str(f_number)+" "+str(accuracy)+" "+str(diff_precent)+" "+"b"+str(i))
        res[i].append(accuracy_score(test_data['b'+str(i)],y_pred['b'+str(i)]))
        res[i].append(precision_score(test_data['b'+str(i)],y_pred['b'+str(i)],average=accuracy))
        res[i].append(recall_score(test_data['b'+str(i)],y_pred['b'+str(i)],average=accuracy))

    '''for i in range(100,len(y_pred)+100):
        print(test_data.loc[[i]])
        print(y_pred.loc[[i]])
        print("***********")'''
    return res