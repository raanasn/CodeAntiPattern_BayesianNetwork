from xml.dom import minidom
def parseXMI(my_file):
	classList=[]
	packageList=[]
	check=[]
	att_count=0
	attused_count=0
	ope_count=0
	i=0
	j=0
	dam=0
	op_public=0
	xmldoc = minidom.parse(my_file)

	### for package and their classes 	
	for package in xmldoc.getElementsByTagName("UML:Package"):
		packageList.append([])
		packageList[j].append(str(package.getAttribute('xmi.id')))
		packageList[j].append(str(package.getAttribute('name')))
		for element in package.getElementsByTagName("UML:Class"):
			packageList[j].append(str(element.getAttribute('xmi.id')))
		packageList[j].append(j)
		j=j+1

	### for classes
	for element in xmldoc.getElementsByTagName("UML:Class"):
		classList.append([])
		classList[i].append(str(element.getAttribute('xmi.id')))
		classList[i].append(str(element.getAttribute('name')))
		classList[i].append(i)
		### find Attributes of class
		for atr in element.getElementsByTagName("UML:Attribute"):
			if (str(atr.getAttribute('visibility'))=="private") or (str(atr.getAttribute('visibility'))=="protected"):
				dam=dam+1
			check.append(str(atr.getAttribute('name')))
			att_count=att_count+1
	### find operations of class
		for ope in element.getElementsByTagName("UML:Operation"):
			if (str(ope.getAttribute('visibility'))=="private") or (str(atr.getAttribute('visibility'))=="protected"):
				dam=dam+1
			elif (str(ope.getAttribute('visibility'))=="public"):
				op_public=op_public+1
			ope_count=ope_count+1
	### check if operations use attributes of class
		for par in element.getElementsByTagName("UML:Parameter"):
			if str(par.getAttribute('kind'))=="inout" and str(par.getAttribute('name')) in check:
				attused_count=attused_count+1
		classList[i].append(att_count)
		classList[i].append(ope_count)	
		classList[i].append(attused_count)
		classList[i].append(op_public)
		try:
			classList[i].append(dam/float(ope_count+att_count))
		except:
			classList[i].append(0)
		next_child=classList[i][0]
		dit=0
		for element in xmldoc.getElementsByTagName("UML:Generalization"):
			#print "BEGIN ", next_child, str(element.getAttribute('child'))
			if str(element.getAttribute('child')) == next_child:
				dit=dit+1
				next_child=str(element.getAttribute('parent'))
				#print "END ", next_child
		classList[i].append(dit)
		att_count=0
		ope_count=0
		attused_count=0
		dam=0
		op_public=0
		check=[]			
		i=i+1
		

		
	#TqW6RdaGAqBwARel
	#for element in xmldoc.getElementsByTagName("UML:Interface"):
	#	classList.append([])
	#	classList[i].append(str(element.getAttribute('xmi.id')))
	#	classList[i].append(str(element.getAttribute('name')))
	#	classList[i].append(i)
	#	i=i+1

	### make relation-list for the classes. 
	### find the relations and insert them in the matrix
	relation=[];
	relation.append([])
	i=0;

	### generalization
	for element in xmldoc.getElementsByTagName("UML:Generalization"):
		relation.append([])
		relation[i].append('generalization')
		relation[i].append(str(element.getAttribute('parent')))
		relation[i].append(str(element.getAttribute('child')))
		i=i+1

	### aggregations-association,composition,aggregation
	twice=False	
	for e in xmldoc.getElementsByTagName("UML:Association.connection"):
		for element in e.getElementsByTagName("UML:AssociationEnd"):
			if twice==False:
				if str(element.getAttribute('aggregation'))=='none':
					relation[i].append('association')
				else:
					print(str(element.getAttribute('aggregation')))
					relation[i].append(str(element.getAttribute('aggregation')))
			relation[i].append(str(element.getAttribute('participant')))
			twice=True
		i=i+1
		relation.append([])	
		twice=False
	relation=relation[:-1]

	for i in relation:
		for item in classList:
			if i[1]==item[0]:
				i.append(item[2])

	for i in relation:
		for item in classList:
			if i[2]==item[0]:
				i.append(item[2])

	### for removing relations with interfaces
	relation = list(filter(None, relation))
	rLen=len(relation)
	sub=0
	for i in range(rLen):
		i=i-sub
		try:
			gotdata = relation[i]
		except IndexError:
			break
		if len(relation[i])!=5:
			relation.remove(relation[i])
			sub=sub+1


	'''for i in relation:
		if(i[0]=='composite' or i[0]=='aggregate' or i[0]=='generalization'):
			b=i[1]
			i[1]=i[2]
			i[2]=b
			b=i[3]
			i[3]=i[4]
			i[4]=b'''

	
	### make relation-list for the packages. 
	packageRelation=[];
	packageRelation.append([])
	pCounter=0
	first=True
	for item in relation:
		for package in packageList:
			if (item[1] in package[2] and first==False) or (item[2] in package[2] and first==False):
				packageRelation[pCounter].append(package[0])
				first=True
				pCounter=pCounter+1
				packageRelation.append([])
				break
			if (item[1] in package[2] and first) or (item[2] in package[2] and first):
				packageRelation[pCounter].append(package[0])
				first=False

	### Keep just the relations in the packageRelation-list
	packageRelation = list(filter(None, packageRelation))
	pLen=len(packageRelation)
	sub=0
	for i in range(pLen):
		i=i-sub
		try:
			gotdata = packageRelation[i]
		except IndexError:
			break
		if len(packageRelation[i])!=2:
			packageRelation.remove(packageRelation[i])
			sub=sub+1
	
	#delete dublicates in list
	new_packrel=[]
	for i in packageRelation:
		if i not in new_packrel:
			new_packrel.append(i)

	for i in range(len(classList)):
		cp=0
		package_id=""
		for item in packageList:
			if classList[i][0] in item[2]:
				package_id=item[0]
				break
		for item in new_packrel:
			if package_id in item:
				cp=cp+1
		classList[i].append(cp)
	return relation,classList,packageList,new_packrel



