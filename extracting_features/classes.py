class Rel:
	def __init__(self, type_,weight):
		self.type_ = type_
		self.weight = weight 

class Class:
	def __init__(self,id_,features,parents,childs):
		self.id_= id_
		self.features = features
		self.parents = parents
		self.childs = childs

