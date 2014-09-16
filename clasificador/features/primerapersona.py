# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling


def esta_en_primera_persona(tag):
	# determinante en primera persona
	# OR verbo en primera persona
	# OR pronombre en primera persona
	return (tag[0] == 'D' and tag[2] == '1') \
		   or (tag[0] == 'V' and tag[4] == '1') \
		   or (tag[0] == 'P' and tag[2] == '1')


class PrimeraPersona(Feature):
	def __init__(self):
		super(PrimeraPersona, self).__init__()
		self.nombre = 'Primera Persona'
		self.descripcion = 'Esta caracteristica mide si el texto esta expresado en primera persona'

	def calcular_feature(self, tweet):
		tf = Freeling(tweet.texto)
		primera_persona = 0
		for token in tf.tokens:
			if esta_en_primera_persona(token.tag):
				primera_persona += 1

		if len(tf.tokens) == 0:  # FIXME: no debería pasar
			print "Error de tokens vacíos en " + self.nombre + ": ", tweet.texto
			tweet.features[self.nombre] = 0
		else:
			tweet.features[self.nombre] = primera_persona / math.sqrt(len(tf.tokens))
