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
        tweet.features[self.nombre] = tweet.texto.startswith(u"-") or tweet.texto.startswith(u"—")
