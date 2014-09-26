# -*- coding: utf-8 -*-
from __future__ import absolute_import

from pkg_resources import resource_filename
import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import *


class PresenciaAnimales(Feature):
	def __init__(self):
		super(PresenciaAnimales, self).__init__()
		self.nombre = 'Presencia de Animales'
		self.descripcion = 'Esta caracteristica mide la cantidad de animales mencinados contiene el texto'
		self.palabrasAnimales = clasificador.herramientas.utils.obtener_diccionario(
			resource_filename('clasificador.recursos.diccionarios', 'DiccionarioAnimales.txt'))

	def calcular_feature(self, tweet):
		tf = Freeling(tweet)
		cant_palabras_animales = 0
		for token in tf.tokens:
			if (token.token in self.palabrasAnimales) or (token.lemma in self.palabrasAnimales):
				cant_palabras_animales += 1

		if len(tf.tokens) == 0:
			print("Error de tokens vacíos en " + self.nombre + ": ", tweet.texto)
			tweet.features[self.nombre] = 0
		else:
			tweet.features[self.nombre] = cant_palabras_animales / math.sqrt(len(tf.tokens))
