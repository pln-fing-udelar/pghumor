# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.feature import Feature


class Dialogo(Feature):
    def __init__(self):
        super(Dialogo, self).__init__()
        self.nombre = "Dialogo"
        self.descripcion = """
			Esta característica mide si existe en el tweet un diálogo
		"""

    def calcular_feature(self, tweet):
        pass