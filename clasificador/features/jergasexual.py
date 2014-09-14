import math
import sys

import .feature
import herramientas.define
from herramientas.treetagger import *
import herramientas.utils

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
