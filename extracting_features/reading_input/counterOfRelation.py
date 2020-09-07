import re

def counterOfRelation(my_file):
	file=open(my_file,"r")
	classRel=[]
	i=0

#Space
	for line in file:
		classRel.append(line.split(" "))
		i=i+1

#Find Function and Name of first Class 
#If it beginns with C it is dynamic. We have no Information
	for item in classRel:
		new=""
		flag=False
		if item[0][0]=='C':
			for alpha in item[0][::-1]:
				if alpha=='.':
					break
				new=new+alpha
			item[0]=new[::-1]
			new=""
			flag=False
			for alpha in item[1][-3::-1]:
				if alpha=='.':
					break
				new=new+alpha
			item[1]=new[::-1]
		else:
			new=""
			funcCaller=""
			flag=False
			funcFlag=False
			for alpha in item[0][::-1]:
				if alpha=='.' and flag==True:
					flag=False
					break
				elif flag==True:
					new=new+alpha
				elif alpha==':':
					funcFlag=False
					flag=True				
				elif funcFlag==True:
					funcCaller=funcCaller+alpha
				elif alpha=='(':
					funcFlag=True				
				
			item[0]=new[::-1]
			item.append(funcCaller[::-1])	

#Find Function and Name of second Class
			new=""
			funcCallee=""
			flag=False
			funcFlag=False
			for alpha in item[1][::-1]:
				if alpha=='.' and flag==True:
					flag=False
					break
				elif flag==True:
					new=new+alpha
				elif alpha==':':
					funcFlag=False
					flag=True				
				elif funcFlag==True:
					funcCallee=funcCallee+alpha
				elif alpha=='(':
					funcFlag=True				
				
			item[1]=new[::-1]
			item.append(funcCaller[::-1])			

#Count operations between same classes
	result=dict()
	for sublist in classRel:
		if str(sublist[0:2]) not in result:
			result[str(sublist[0:2])]=1
		else:
			result[str(sublist[0:2])]=result[str(sublist[0:2])]+1

	return classRel, result

