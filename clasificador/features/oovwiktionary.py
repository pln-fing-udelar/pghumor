# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling
from clasificador.herramientas.wiktionary import Wiktionary
from clasificador.realidad.tweet import *


CARACTERES_ESPANOL = 255

patron_todo_espacios = re.compile(r'^\s*$', re.UNICODE)


def contiene_caracteres_no_espanoles(texto):
    return any(ord(c) > CARACTERES_ESPANOL for c in texto)


def eliminar_underscores(texto):
    return texto.replace('_', ' ')


class OOVWiktionary(Feature):
    def __init__(self):
        super(OOVWiktionary, self).__init__()
        self.nombre = "OOV Wiktionary"
        self.descripcion = """
            Cuenta la cantidad de palabras fuera del vocabulario de Freeling y Wiktionary que contiene el texto.
        """

    def calcular_feature(self, tweet):
        texto = tweet.texto
        texto = remover_hashtags(texto)
        texto = remover_usuarios(texto)
        oraciones = Freeling.procesar_texto(texto)
        tokens = list(itertools.chain(*oraciones))

        cant_palabras_oov = 0
        for token_freeling in tokens:
            token = eliminar_underscores(token_freeling.token)
            if not Wiktionary.pertenece(token):
                cant_palabras_oov += 1

        if len(tokens) == 0:
            return 0
        else:
            return cant_palabras_oov / math.sqrt(len(tokens))
