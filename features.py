
#rel: relation-list of one class
#class_properties: class_properties of one class
#wb: bad smell excel

def get_features(rel,class_properties,wb):
	#AMW
	amw=0
	var=0
	for item in rel:
		var=var+item[7]
	try:
		amw=var/len(rel)
	except:
		amw=0
	
	#Relation
	relation=len(rel)
	
	#DIT
	dit=class_properties[8]
	
	#NOM
	nom=class_properties[4]

	#LCOM ya LCOMHS
	lcom=0
	lcomHS=0
	F=float(class_properties[3])
	M=float(class_properties[4])
	MyF=float(class_properties[5])
	try:
		lcom=1-((1/(F*M))*MyF)
	except:
		lcom=100
	try:
		lcomHS=(1/(M-1))*(M-((1/F)*MyF))
	except:
		lcomHS=100
	
	#DAM
	dam= class_properties[6]
	
	#NAM
	nam=class_properties[7]
	
	#CP
	#cp=class_properties[9]
	
	#cycle
	cycle=0
	for r in rel:
		if r[1] == r[2]:
			cycle=1
			print(class_properties[2])
			break

	#Bad Smells
	#GodCLass - name of the classes with smell
	badsmells=[0,0,0,0]
	for item in range(0,4):
		sheet = wb.sheet_by_index(item)
		for row_num in range(sheet.nrows):
			row_value = sheet.row_values(row_num)
			for r in row_value:
				r_=r.split('.')
				if class_properties[1] == r or class_properties[1]==r[:-1] or class_properties[1]==r[:-2] or class_properties[1] == r_[-1] or class_properties[1]==r_[-1][:-1] or class_properties[1]==r_[-1][:-2]:
					badsmells[item]=1
					break
			if badsmells[item]==1:
				break
	
	#print("AMW, DIT, NOM, LCOM, REL, DAM ,NAM, CYCLE, BADSMELLS")
			
	features=[amw,dit,nom,lcom,relation,dam,nam,cycle,badsmells]
	return features
