# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.feature import Feature


class Preguntas(Feature):
	def __init__(self):
		super(Preguntas, self).__init__()
		self.nombre = "Preguntas"
		self.descripcion = """
			Esta característica mide si existe en el tweet preguntas y respuestas
		"""

	def calcular_feature(self, tweet):
		pass