# coding=utf-8
from __future__ import absolute_import, unicode_literals

import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling


class Negacion(Feature):
    def __init__(self):
        super(Negacion, self).__init__()
        self.nombre = "Negacion"
        self.descripcion = """
            Cuenta la cantidad de palabras 'no' en el tweet.
        """

    def calcular_feature(self, tweet):
        freeling = Freeling(tweet)

        negaciones = 0
        for token in freeling.tokens:
            if token.token.lower() == 'no':
                negaciones += 1

        if len(freeling.tokens) == 0:
            return 0
        else:
            return negaciones / math.sqrt(len(freeling.tokens))
