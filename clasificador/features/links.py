# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math

from clasificador.features.feature import Feature


class Links(Feature):
    def __init__(self):
        super(Links, self).__init__()
        self.nombre = "Links"
        self.descripcion = """
            Cuenta la cantidad de links presentes
        """

    def calcular_feature(self, tweet):
        tweet.features[self.nombre] = tweet.cantidad_links()

