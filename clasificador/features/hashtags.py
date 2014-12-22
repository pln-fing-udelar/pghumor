# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from clasificador.features.feature import Feature


class Hashtags(Feature):
    def __init__(self):
        super(Hashtags, self).__init__()
        self.nombre = "Hashtags"
        self.descripcion = """
            Cuenta la cantidad de hashtags.
        """

    def calcular_feature(self, tweet):
        return tweet.cantidad_hashtags()

