# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling


class PalabrasMayusculas(Feature):
    def __init__(self):
        super(PalabrasMayusculas, self).__init__()
        self.nombre = "PalabrasMayusculas"
        self.descripcion = """
            Cuenta la cantidad de palabras totalmente en mayúsculas, resaltando conceptos.
        """

    def calcular_feature(self, tweet):
        freeling = Freeling(tweet)

        tokens_no_puntuacion = 0
        tokens_en_mayusculas = 0

        for token in freeling.tokens:
            tokens_no_puntuacion += 1
            if token.tag[0] != 'F' and token.token == token.token.upper():
                tokens_en_mayusculas += 1

        if len(tokens_no_puntuacion) == 0:
            return 0
        else:
            return tokens_en_mayusculas / tokens_no_puntuacion
