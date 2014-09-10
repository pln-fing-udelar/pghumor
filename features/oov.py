import math
import sys

sys.path.append("../herramientas")

import feature
from treetagger import *

class OOV(feature.Feature):

	def __init__(self):
		self.nombre = "OOV"

	def calcularFeature(self, tweet):
		tt = TreeTagger(tweet.texto)
		cantPalabrasOOV = 0
		for token in tt.tokens:
			if token.lemma == '<unknown>':
				cantPalabrasOOV += 1

		tweet.features[self.nombre] = cantPalabrasOOV/math.sqrt(len(tt.tokens))
