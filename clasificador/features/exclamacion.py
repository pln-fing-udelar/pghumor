# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.feature import Feature


class Exclamacion(Feature):
    def __init__(self):
        super(Exclamacion, self).__init__()
        self.nombre = "Exclamacion"
        self.descripcion = """
            Mide si existen exclamaciones en el tweet o palabras totalmente en mayúscula resaltando un concepto.
        """

    def calcular_feature(self, tweet):
        pass
