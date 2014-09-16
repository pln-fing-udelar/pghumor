# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math
import sys

from features.feature import Feature
import herramientas.define
from herramientas.treetagger import TreeTagger
import herramientas.utils

class JergaSexual(Feature):

	def __init__(self):
		self.nombre = 'Jerga Sexual'
		self.descripcion = 'Esta caracteristica mide la cantidad de jerga sexual que contiene el texto'
		self.palabrasSexuales = herramientas.utils.obtenerDiccionario('diccionarios/' + herramientas.define.PATH_DICCIONARIO_SEXUAL)
		
	def calcular_feature(self, tweet):
		tt = TreeTagger(tweet.texto)
		cant_palabras_sexuales = 0
		for token in tt.tokens:
			if (token.token in self.palabrasSexuales) or (token.lemma in self.palabrasSexuales):
				cant_palabras_sexuales += 1

		if len(tt.tokens) == 0:
			print "Error de tokens vacíos en " + self.nombre + ": ", tweet.texto
			tweet.features[self.nombre] = 0
		else:
			tweet.features[self.nombre] = cant_palabras_sexuales/math.sqrt(len(tt.tokens))
