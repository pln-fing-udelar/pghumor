# coding=utf-8
from __future__ import absolute_import, division, unicode_literals
import re

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling

patron_palabra = re.compile(r'\b\w+\b', re.UNICODE)


class PalabrasMayusculas(Feature):
    def __init__(self):
        super(PalabrasMayusculas, self).__init__()
        self.nombre = "PalabrasMayusculas"
        self.descripcion = """
            Cuenta la cantidad de palabras totalmente en mayúsculas, dividido la cantidad de palabras del tweet.
        """

    def calcular_feature(self, tweet):
        freeling = Freeling(tweet)

        tokens_no_puntuacion = 0

        for token in freeling.tokens:
            if token.tag[0] != 'F':
                tokens_no_puntuacion += 1

        palabras_en_mayusculas = 0
        for palabra in patron_palabra.findall(tweet.texto):
            if palabra == palabra.upper():
                palabras_en_mayusculas += 1

        if tokens_no_puntuacion == 0:
            if palabras_en_mayusculas > 0:
                print("ERROR: en el tweet \"" + tweet.texto + "\" no se encontraron tokens de no puntuación con"
                                                              " Freeling, pero se encontraron palabras en mayúsculas con expresiones regulares.")
            return 0
        else:
            return palabras_en_mayusculas / tokens_no_puntuacion
