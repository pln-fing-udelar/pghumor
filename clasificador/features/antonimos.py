# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math

from clasificador.features.feature import Feature

from nltk.corpus import WordNetCorpusReader
from clasificador.herramientas.freeling import Freeling
from clasificador.realidad.tweet import remover_hashtags, remover_usuarios

from pkg_resources import resource_filename


class Antonimos(Feature):
	def __init__(self):
		super(Antonimos, self).__init__()
		self.nombre = 'Antonimos'
		self.descripcion = 'Esta caracteristica mide la cantidad de pares de antónimos presentes en el texto.'

		self.wncr = WordNetCorpusReader(resource_filename('clasificador.recursos', 'wordnet_spa'))

	def calcular_feature(self, tweet):
		tokens = Freeling.procesar_texto(remover_hashtags(remover_usuarios(tweet.texto)))

		cant_antonimos = 0

		for token in tokens:
			antonimos = []
			for synset in self.wncr.synsets(token.lemma):
				for lemma in synset.lemmas:
					antonimos += [lemma_antonimo.name for lemma_antonimo in lemma.antonyms()]

			for otro_token in tokens:
				if otro_token.lemma in antonimos:
					cant_antonimos += 1
					break

		if len(tokens) == 0:
			tweet.features[self.nombre] = 0
		else:
			tweet.features[self.nombre] = cant_antonimos / math.sqrt(len(tokens))
