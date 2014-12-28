# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import regex  # Soporta pedirle letras en mayúsculas unicode, mientras que re no.

from clasificador.features.feature import Feature

patron_palabra_o_numero = regex.compile(r'\b\w+\b', regex.UNICODE)
patron_palabra_mayuscula = regex.compile(r'\b\p{Lu}+\b', regex.UNICODE)


class PalabrasMayusculas(Feature):
    def __init__(self):
        super(PalabrasMayusculas, self).__init__()
        self.nombre = "PalabrasMayusculas"
        self.descripcion = """
            Cuenta la cantidad de palabras totalmente en mayúsculas, dividido la cantidad de palabras del tweet.
        """

    def calcular_feature(self, tweet):
        palabras_o_numeros = len(patron_palabra_o_numero.findall(tweet.texto))
        palabras_en_mayusculas = len(patron_palabra_mayuscula.findall(tweet.texto))

        if palabras_o_numeros == 0:
            return 0
        else:
            return palabras_en_mayusculas / palabras_o_numeros
