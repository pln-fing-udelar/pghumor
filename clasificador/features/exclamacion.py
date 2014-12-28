# coding=utf-8
from __future__ import absolute_import, unicode_literals

import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling


class Exclamacion(Feature):
    def __init__(self):
        super(Exclamacion, self).__init__()
        self.nombre = "Exclamacion"
        self.descripcion = """
            Cuenta la cantidad de signos de exclamación en el tweet,
            dividido la raíz de la cantidad de tokens del tweet.
        """

    def calcular_feature(self, tweet):
        freeling = Freeling(tweet)

        exclamaciones = 0
        for token in freeling.tokens:
            if token.tag == 'Fat' or token.tag == 'Faa':
                exclamaciones += 1

        if len(freeling.tokens) == 0:
            return 0
        else:
            return exclamaciones / math.sqrt(len(freeling.tokens))
