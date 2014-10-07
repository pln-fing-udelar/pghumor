# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.feature import Feature


class Preguntas(Feature):
	def __init__(self):
		super(Preguntas, self).__init__()
		self.nombre = "Exclamacion"
		self.descripcion = """
			Esta característica mide si existe en el tweet Exlamaciones y palabras totalmente en mayuscula resaltando un concepto
		"""

	def calcular_feature(self, tweet):
		pass