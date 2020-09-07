import itertools
import pickle
from PGM_Model.model import *
from PGM_Model.output import *

def test_data(name,len_f,diff_precent,accuracy,f_number,properties,split,sheet,structure):#len_f=special range, f_number=special f
    #!!!featre length is in the first loop written with hand (8)
    #!!!len_bs is written with hand

    len_bs = 4
    all_smells = []
    all_smells=[list() for x in range(len_bs)]
    other_structure = []
    #Reading Data
    class_objects = pickle.load(open("Pickle/classes"+name+".pkl", "rb"))
    '''alaki_godclass=0
    alaki_dataclass=0
    alaki_featureenvy=0
    for alaki in class_objects:
        alaki_godclass+=alaki.features[8][0]
        alaki_dataclass+=alaki.features[8][1]
        alaki_featureenvy += alaki.features[8][2]'''
    #Making data ready for Panda
    all_features=[]
    for class_ in class_objects:
       kasr=0
       zarib=[]
       f=[]
       if properties=="smells":
           flag=False
           for s in range(len_bs):
               if class_.features[8][s]==1:#THIS AND
                   flag=True
           if flag==False:
               continue
       bayesian_structure=[]
       if structure == "child" or structure=="child2":
           bayesian_structure=class_.childs
       else:
           bayesian_structure=class_.parents
       for parent in bayesian_structure:
          kasr=parent[1].weight + kasr #has to go one round alone
          zarib.append(parent[1].weight)
       for i in range(8):# this AND
          foo=0
          for p,z in zip(bayesian_structure,zarib):
             foo=(p[0].features[i]*z/kasr)+foo
          f.append(foo)
       if class_.features[7] == 1:#cycle (its his issue not his parents or childs) THIS AND
           f[7]=1
       all_features.append(f)
       for bs in range(len_bs):
           all_smells[bs].append(class_.features[8][bs]) #This END

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

    if f_number!=[] and properties!="equal":
        for i in range(len(f_number)):
            features.append([])
        arr=len(features)
        for f in all_features:
            for fn,ar in zip(f_number,range(arr)):
                if f[fn] >= diff[fn]:
                    features[ar].append(1)
                else:
                    features[ar].append(0)
        if structure=="child2":
            return features
        elif structure=="both":
            other_structure = test_data(name, len_f, diff_precent, accuracy, f_number, properties, split, sheet,"child2")
        res = model(features, all_smells, properties, len_bs, len_f, f_number, accuracy,split,structure,other_structure)
    elif properties != "equal":
        for i in range(len_f):
            features.append([])
        for f in all_features:
            for i in range(len_f):
                if f[i] >= diff[i]:
                    features[i].append(1)
                else:
                    features[i].append(0)
        if structure=="child2":
            return features
        elif structure=="both":
            other_structure = test_data(name, len_f, diff_precent, accuracy, f_number, properties, split, sheet,"child2")
        res=model(features,all_smells,properties,len_bs,len_f,f_number,accuracy,split,structure,other_structure)
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
        if f_number!=[]:
            for b in range(len_bs):
                for item in reversed(range(len_f)):
                    if item not in f_number:
                        del equal_f[b][item]
        child_feature=[]
        for number in range(len_bs):
            if structure == "child2":
                child_feature.append(equal_f[number])
            elif structure == "both":
                other_structure = test_data(name, len_f, diff_precent, accuracy, f_number, properties, split, sheet,"child2")
            if structure!="child2":
                if len(other_structure)==0:
                    other_structure=[list() for x in range(len_bs)]
                res.append(model(equal_f[number], equal_smells[number], properties, len_bs, len_f, f_number, accuracy,split,structure,other_structure[number]))
        if structure=="child2":
            return child_feature
    excel(name,f_number,diff_precent,split,len_bs,res,sheet)
    return
