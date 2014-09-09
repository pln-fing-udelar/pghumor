import math
import sys

import Feature
sys.path.append("../Herramientas")
from TreeTagger import *
import define
import utils


FEATURE_NAME="Jerga Sexual"

class JergaSexual(Feature.Feature):

	def __init__(self):
		self.palabrasSexuales = utils.obtenerDiccionario("../Diccionarios/" + define.PATH_DICCIONARIO_SEXUAL)
		
	def calcularFeature(self, tweet):

		tt = TreeTagger(tweet.texto)
		cantPalabrasSexuales = 0
		for token in tt.tokens:
			if (token.token in self.palabrasSexuales) or (token.lemma in self.palabrasSexuales):
				cantPalabrasSexuales = cantPalabrasSexuales + 1

		tweet.features[FEATURE_NAME] = cantPalabrasSexuales/math.sqrt(len(tt.tokens))