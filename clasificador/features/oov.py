# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math
import sys

from features.feature import Feature
from herramientas.treetagger import *

class OOV(Feature):

	def __init__(self):
		self.nombre = "OOV"

	def calcularFeature(self, tweet):
		tt = TreeTagger(tweet.texto)
		cantPalabrasOOV = 0
		for token in tt.tokens:
			if token.lemma == '<unknown>':
				cantPalabrasOOV += 1

		if len(tt.tokens) == 0: # FIXME: no debería pasar
			print "Error: ", tweet.texto
			tweet.features[self.nombre] = 0
		else:
			tweet.features[self.nombre] = cantPalabrasOOV/math.sqrt(len(tt.tokens))
