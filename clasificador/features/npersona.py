# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling


def esta_en_persona(tag, numero_persona):
    # determinante en 'numeroPersona' persona
    # OR verbo en primera persona
    # OR pronombre en primera persona
    return (tag[0] == 'D' and tag[2] == str(numero_persona)) or\
           (tag[0] == 'V' and tag[4] == str(numero_persona)) or\
           (tag[0] == 'P' and tag[2] == str(numero_persona))


class NPersona(Feature):
    def __init__(self, persona):
        super(NPersona, self).__init__()
        self.persona = persona

    def calcular_feature(self, tweet):
        tf = Freeling(tweet)
        primera_persona = 0
        for token in tf.tokens:
            if esta_en_persona(token.tag, self.persona):
                primera_persona += 1

        if len(tf.tokens) == 0:
            print("Error de tokens vacíos en " + self.nombre + ": ", tweet.texto)
            return 0
        else:
            return primera_persona / math.sqrt(len(tf.tokens))
