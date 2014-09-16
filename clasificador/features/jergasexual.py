# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math

from clasificador.features.feature import Feature
import clasificador.herramientas.define
from clasificador.herramientas.treetagger import TreeTagger
import clasificador.herramientas.utils

from pkg_resources import resource_filename


class JergaSexual(Feature):
	def __init__(self):
		super(JergaSexual, self).__init__()
		self.nombre = 'Jerga Sexual'
		self.descripcion = 'Esta caracteristica mide la cantidad de jerga sexual que contiene el texto'
		self.palabrasSexuales = clasificador.herramientas.utils.obtener_diccionario(
			resource_filename('clasificador.recursos.diccionarios', 'DiccionarioSexual.txt'))

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
			tweet.features[self.nombre] = cant_palabras_sexuales / math.sqrt(len(tt.tokens))
