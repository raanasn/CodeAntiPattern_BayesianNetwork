from parse import *
from parse2 import *
from counterOfRelation import*

def input_(xmi,rel,type):

	if type == "1.2":
		relation, classList, packageList, packageRelation= parseXMI(xmi)
	elif type == "2":
		relation, classList, packageList, packageRelation = parseXMI2(xmi)

	allRelFunc, counterOfRel=counterOfRelation(rel)

	for rel in relation:
			for Class in classList:
				if rel[3]==Class[2]:
					rel.append(Class[1])
					break;
			for Class in classList:
				if rel[4]==Class[2]:
					rel.append(Class[1]) 
					break;

	### Join Relation and Counter
	for rel in relation:
		if str(rel[5:7]) in counterOfRel:
			rel.append(counterOfRel[str(rel[5:7])])

	#Maybe we have some repeatet associations, we add them to the counter	

	l=[]
	repeat=[]
	for i in relation:
		if i in l:
			repeat.append(i)
		else:
			l.append(i)

	mainRelation=[]
	for sublist in l:
		if sublist not in mainRelation and len(sublist)!=8:
			sublist.append(1)
			mainRelation.append(sublist)
		elif sublist not in mainRelation and len(sublist)==8:
			mainRelation.append(sublist)

	for item in repeat:
		for rel in mainRelation:
			if item[0:7] == rel[0:7]:
				rel[7]=rel[7]+1
				break
	return mainRelation, classList



