import math
import sys

sys.path.append("../herramientas")

import define
import feature
from treetagger import *
import utils

class JergaSexual(feature.Feature):

	def __init__(self):
		self.nombre = 'Jerga Sexual'
		self.palabrasSexuales = utils.obtenerDiccionario('../diccionarios/' + define.PATH_DICCIONARIO_SEXUAL)
		
	def calcularFeature(self, tweet):
		tt = TreeTagger(tweet.texto)
		cantPalabrasSexuales = 0
		for token in tt.tokens:
			if (token.token in self.palabrasSexuales) or (token.lemma in self.palabrasSexuales):
				cantPalabrasSexuales += 1

		tweet.features[self.nombre] = cantPalabrasSexuales/math.sqrt(len(tt.tokens))
