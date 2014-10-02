from __future__ import absolute_import

import clasificador.herramientas.utils
import re


class Freeling:
	cache = {}

	def __init__(self, tweet):
		if tweet.id not in Freeling.cache:
			self.tokens = Freeling.procesar_texto(tweet.texto_original)
			Freeling.cache[tweet.id] = self
		else:
			self.tokens = Freeling.cache[tweet.id].tokens

	@staticmethod
	def procesar_texto(texto):
		command = 'echo "' + clasificador.herramientas.utils.escapar(texto) + '" | analyzer_client 55555'
		resultado = clasificador.herramientas.utils.ejecutar_comando(command)
		tokens = []
		for line in resultado:
			matcheo = re.search('^(.*)\s(.*)\s(.*)\s(.*)\n', line)
			if matcheo is not None:
				detalle = TokenFL()
				detalle.token = matcheo.group(1)
				detalle.lemma = matcheo.group(2)
				detalle.tag = matcheo.group(3)
				detalle.probabilidad = matcheo.group(4)
				tokens.append(detalle)
		return tokens


# DataType
class TokenFL:
	def __init__(self):
		self.token = ""
		self.tag = ""
		self.lemma = ""
		self.probabilidad = ""
