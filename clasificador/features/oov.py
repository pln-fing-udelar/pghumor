# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math

from features.feature import Feature
from herramientas.treetagger import *


class OOV(Feature):

	def __init__(self):
		self.nombre = "OOV"

	def calcular_feature(self, tweet):
		tt = TreeTagger(tweet.texto)
		cant_palabras_oov = 0
		for token in tt.tokens:
			if token.lemma == '<unknown>':
				cant_palabras_oov += 1

		if len(tt.tokens) == 0:
			print "Error: ", tweet.texto
			tweet.features[self.nombre] = 0
		else:
			tweet.features[self.nombre] = cant_palabras_oov/math.sqrt(len(tt.tokens))
