

class Feature:
	
	def __init__(self):
		self.nombre = ""
		self.descripcion = ""

	def calcularFeature(self, tweet):
		raise NotImplementedError
