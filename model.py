import pandas as pd
import numpy as np
from pgmpy.models import BayesianModel
from sklearn.metrics import f1_score, accuracy_score, precision_score, recall_score

#bs is written with hand

def shuffle(df, n=1, axis=0):
    df = df.copy()
    for _ in range(n):
        df.apply(np.random.shuffle, axis=axis)
    return df

def model(features,all_smells,properties,len_bs,len_f,f_number,accuracy,diff_precent,split):
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
    if f_number!=[] and properties!="equal":
        for i in range(len_bs):
            for j in f_number:
                model.add_edge('f' + str(j), 'b' + str(i))
    elif properties!="equal":
        for i in range(len_bs):  # badsmell
            for j in range(len_f):  # feature
                model.add_edge('f' + str(j), 'b'+str(i))
    elif f_number==[] and properties=="equal":
        for j in range(len_f):  # feature
            model.add_edge('f' + str(j), 'b')
    elif f_number!=[] and properties=="equal":
        for j in f_number:  # feature
            model.add_edge('f' + str(j), 'b')

    values=shuffle(values)
    train_data = values[:int((len(all_smells)*split))]
    test_data  = values[int((len(all_smells)*split)):]
    predict_data = test_data.copy()

    delete=[]
    if f_number==[]:
        for f in range(len_f):
            if (train_data['f'+str(f)] == 0).all():
                delete.append(f)
    else:
        for f in f_number:
            if (train_data['f'+str(f)] == 0).all():
                delete.append(f)
    for item in delete:
        del train_data['f'+str(item)]
        del predict_data['f' + str(item)]
        model.remove_node('f'+str(item))

    if f_number!=[] and properties!="equal":
        predict_data.drop(['b0', 'b1', 'b2'], axis=1, inplace=True)
        for i in f_number:
            test_data.drop(['f' + str(i)], axis=1, inplace=True)
    elif properties!="equal":
        predict_data.drop(['b0','b1','b2'], axis=1, inplace=True)
        for i in range(len_f):
            test_data.drop(['f' + str(i)], axis=1, inplace=True)
    elif properties=="equal":
        predict_data.drop(['b'], axis=1, inplace=True)
        if f_number==[]:
            for i in range(len_f):
                test_data.drop(['f' + str(i)], axis=1, inplace=True)
        else:
            for i in f_number:
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