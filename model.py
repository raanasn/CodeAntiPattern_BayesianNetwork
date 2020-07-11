import pandas as pd
import numpy as np
from pgmpy.models import BayesianModel
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

#!!!bs is written with hand
#!!!crossed is done by hand

def shuffle(df, n=1, axis=0):
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df

def model(features,all_smells,properties,len_bs,len_f,f_number,accuracy,split,structure,other_features):
    if properties=="equal":
        values = pd.DataFrame(data={'b': all_smells})
    else:
        values=pd.DataFrame(data={'b0': all_smells[0],'b1': all_smells[1],'b2':all_smells[2]})

    if f_number!=[]:
        for i,j in zip(f_number,range(len(features))):
            d = pd.DataFrame({'f' + str(i): features[j]})
            values = pd.concat([values, d], axis=1)
            if structure=="both" and other_features!=[[]]:
                d2 = pd.DataFrame({'c' + str(i): other_features[j]})
                values = pd.concat([values, d2], axis=1)
    else:
        for i in range(len_f):
            d=pd.DataFrame({'f'+str(i):features[i]})
            values = pd.concat([values, d], axis=1)
            if structure=="both" and other_features!=[[]]:
                d2 = pd.DataFrame({'c' + str(i): other_features[i]})
                values = pd.concat([values, d2], axis=1)

    values=shuffle(values)
    crossed = np.split(values.sample(frac=1),
                       [int(.2 * len(values)), int(.4 * len(values)), int(.6 * len(values)), int(.8 * len(values))])
    res = []
    for cross in range(split):
        model = BayesianModel()
        if f_number != [] and properties != "equal":
            for i in range(len_bs):
                for j in f_number:
                    if structure=="child":
                        model.add_edge('b' + str(i), 'f' + str(j))
                    elif structure=="parent" or other_features==[[]]:
                        model.add_edge('f' + str(j), 'b' + str(i))
                    elif structure =="both":
                        model.add_edge('f' + str(j), 'b' + str(i))
                        model.add_edge('b' + str(j), 'c' + str(i))
        elif properties != "equal":
            for i in range(len_bs):  # badsmell
                for j in range(len_f):  # feature
                    if structure=="child":
                        model.add_edge('b' + str(i), 'f' + str(j))
                    elif structure=="parent" or other_features==[[]]:
                        model.add_edge('f' + str(j), 'b' + str(i))
                    elif structure=="both":
                        model.add_edge('f' + str(j), 'b' + str(i))
                        model.add_edge('b' + str(j), 'c' + str(i))
        elif f_number == [] and properties == "equal":
            for j in range(len_f):  # feature
                if structure=="child":
                    model.add_edge('b', 'f' + str(j))
                elif structure=="parent" or other_features==[[]]:
                    model.add_edge('f' + str(j), 'b')
                elif structure=="both":
                    model.add_edge('f' + str(j), 'b')
                    model.add_edge('b', 'c' + str(j))
        elif f_number != [] and properties == "equal":
            for j in f_number:  # feature
                if structure=="child":
                    model.add_edge('b', 'f' + str(j))
                elif structure=="parent" or other_features==[[]]:
                    model.add_edge('f' + str(j), 'b')
                elif structure=="both":
                    model.add_edge('f' + str(j), 'b')
                    model.add_edge('b', 'c' + str(j))

        test_data=crossed[cross]
        train_data=pd.DataFrame()
        for c in range(split):
            if c!=cross:
                train_data = pd.concat([train_data, crossed[c]])

        predict_data = test_data.copy()

        delete=[]
        delete_c=[]
        error_res=[]
        if f_number==[]:
            for f in range(len_f):
                if (train_data['f'+str(f)] == 0).all() or (train_data['f'+str(f)] == 1).all():
                    delete.append(f)
                if structure=="both":
                    if (train_data['c'+str(f)] == 0).all() or (train_data['c'+str(f)] == 1).all():
                        delete_c.append(f)
        else:
            for f in f_number:
                if (train_data['f'+str(f)] == 0).all() or (train_data['f'+str(f)] == 1).all():
                    delete.append(f)
                if structure=="both":
                    if (train_data['c'+str(f)] == 0).all() or (train_data['c'+str(f)] == 1).all():
                        delete_c.append(f)

        for item in delete:
            del train_data['f'+str(item)]
            del predict_data['f' + str(item)]
            model.remove_node('f'+str(item))

        for item in delete_c:
            del train_data['c'+str(item)]
            del predict_data['c' + str(item)]
            model.remove_node('c'+str(item))
        #if all fs are deleted or predict has no value
        if len(train_data.columns)==1 or predict_data.empty:
            continue

        if properties=="equal":
            predict_data.drop(['b'], axis=1, inplace=True)
            test_data = test_data[['b']]
        else:
            predict_data.drop(['b0', 'b1', 'b2'], axis=1, inplace=True)
            test_data = test_data[['b0', 'b1', 'b2']]
        model.fit(train_data)

        y_pred = model.predict(predict_data)
        precent_pred=model.predict_probability(predict_data)

        if properties=="equal":
            r=[]
            #r.append("cross"+str(cross))
            r.append(precision_score(test_data['b'], y_pred['b'], average=accuracy))
            r.append(recall_score(test_data['b'], y_pred['b'], average=accuracy))
            r.append(delete)
            res.append(r)
            '''print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
            for ((index, row),(index2,row2)) in zip(test_data.iterrows(), y_pred.iterrows()):
                print(row['b'],row2['b'])
                print("***********")'''
        else:
            for i in range(len_bs):
                res.append([])
                res[i].append(precision_score(test_data['b'+str(i)],y_pred['b'+str(i)],average=accuracy))
                res[i].append(recall_score(test_data['b'+str(i)],y_pred['b'+str(i)],average=accuracy))
                res[i].append(delete)
    return res