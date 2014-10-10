# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling

import math


class Exclamacion(Feature):
    def __init__(self):
        super(Exclamacion, self).__init__()
        self.nombre = "Exclamacion"
        self.descripcion = """
            Mide si existen exclamaciones en el tweet o palabras totalmente en mayúscula resaltando un concepto.
        """

    def calcular_feature(self, tweet):
        freeling = Freeling(tweet)

        feature = 0
        for token in freeling.tokens:
            if token.tag == 'Fat':
                feature += 1

        #if token.token == token.token.upper():
        #    feature

        if len(freeling.tokens) == 0:
            tweet.features[self.nombre] = 0
        else:
            tweet.features[self.nombre] = feature / math.sqrt(len(freeling.tokens))
