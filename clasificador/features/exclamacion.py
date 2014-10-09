# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.feature import Feature


class Exclamacion(Feature):
    def __init__(self):
        super(Exclamacion, self).__init__()
        self.nombre = "Exclamacion"
        self.descripcion = """
            Esta característica mide si existe en el tweet exlamaciones
            y palabras totalmente en mayúscula resaltando un concepto.
        """

    def calcular_feature(self, tweet):
        pass
