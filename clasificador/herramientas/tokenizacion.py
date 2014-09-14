# -*- coding: UTF-8 -*-
from __future__ import absolute_import

import nltk

def tokenizar(texto):
	#texto = u'Esta es una prueba. Hola, ¿cómo andas? Hoy es lunes 01/09/2014 y son las 14:24. Ayer comí 3 panchos. Me llamo José Gervasio Artigas. Racing ayer ganó 3 a 1. En fin... Ahora pruebo los paréntesis (o no), o sí. Ahorrá $99.98 o la coma es $99,98 papi. El 50% de la gente que mira televisión son la mitad. Soy semi-gay. El perro del vecino.'

	detector_de_sentencias = nltk.data.load('tokenizers/punkt/spanish.pickle')

	oraciones = detector_de_sentencias.tokenize(texto)

	return [nltk.word_tokenize(oracion) for oracion in oraciones]
