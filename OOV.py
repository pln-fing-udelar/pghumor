

import Feature
from TreeTagger import *

FEATURE_NAME="OOV"

class JergaSexual(Feature.Feature):

	def __init__(self):
		pass

	def calcularFeature(self, tweet):

		tt = TreeTagger(tweet.texto)
		cantPalabrasOOV = 0
		for token in tt.tokens:
			if (token.lemma = '<unknown>'):
				cantPalabrasOOV = cantPalabrasOOV + 1

		tweet.features[FEATURE_NAME] = cantPalabrasOOV/math.sqrt(len(tt.tokens))
