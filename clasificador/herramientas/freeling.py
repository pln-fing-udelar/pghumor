from __future__ import absolute_import

import herramientas.utils
import re

class Freeling:

	def __init__(self, texto):
		command = 'echo "' + herramientas.utils.escapar(texto) + '" |  analyzer_client 55555'
		resultado = herramientas.utils.ejecutarComando(command)
		self.tokens = []
		for line in resultado:
			matcheo = re.search('^(.*)\s(.*)\s(.*)\s(.*)\n', line)
			if matcheo != None:
				detalle = TokenFL()
				detalle.token = matcheo.group(1)
				detalle.lemma = matcheo.group(2)
				detalle.tag = matcheo.group(3)
				detalle.probabilidad = matcheo.group(4)
				self.tokens.append(detalle)

#DataType
class TokenFL:

	def __init__(self):
		self.token = ""
		self.tag = ""
		self.lemma = ""
		self.probabilidad = ""
