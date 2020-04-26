from input import *
from classes import *
from features import *
import xlrd
import pickle

xmifiles=['freemindt src a 1.2 xmi.xmi','jag 6.1 source xmi.xmi','jgraphsrc a 1.2 xmi.xmi','Junit1.2.xmi']
relfiles=['freemindREL.txt','Jag.txt','JGraph.txt','Junit.txt']
excelfiles=["Freemind.xlsx",'Jag.xlsx','JGraph.xlsx','Junit.xlsx']
names=["_freemind","_jag",'_jgraph','_junit']

for xmi_fil,rel_fil,excel_fil,nam in zip(xmifiles,relfiles,excelfiles,names):
	xmi_file="Input/"+xmi_fil
	rel_file="Input/"+rel_fil
	excel_file="Input/"+excel_fil
	name=nam

	#Reading the input files
	rels, classes =input_(xmi_file,rel_file)
	smells = xlrd.open_workbook(excel_file)
	class_objects=[]

	for class_ in classes:
		rel=[x for x in rels if class_[0] in x]
		c = Class(str(class_[2])+name,get_features(rel,class_,smells),[],[])
		class_objects.append(c)

	for i in range(len(class_objects)):
		childs=[]
		parents=[]
		rel=[x for x in rels if classes[i][0] in x]
		for r in rel:
			r_=Rel(r[0],r[7])
			if r[1] == r[2]:
				continue
			elif r[1] == classes[i][0]:
				c=class_objects[int(r[4])]
				#for c in class_objects:
				#		if c.id==r[2]+name:
				#			class_inrel=c
				#			break
				if r[0]=="association":
					childs.append([c,r_])
				else:
					parents.append([c,r_])
			elif r[2] == classes[i][0]:
				c=class_objects[int(r[3])]
				#for c in class_objects:
				#		if c.id==r[1]:
				#			class_inrel=c
				#			break
				if r[0]=="association":
					parents.append([c,r_])
				else:
					childs.append([c,r_])
		class_objects[i].parents=parents
		class_objects[i].childs=childs


	with open('classes'+name+'.pkl', 'wb') as f:
		pickle.dump(class_objects, f)




