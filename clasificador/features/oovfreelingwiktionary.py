# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling
from clasificador.herramientas.utils import eliminar_underscores
from clasificador.herramientas.wiktionary import Wiktionary
from clasificador.realidad.tweet import *


class OOV(Feature):
    def __init__(self):
        super(OOV, self).__init__()
        self.nombre = "OOV Freeling Wiktionary"
        self.descripcion = """
            Mide la cantidad de palabras fuera del vocabulario que contiene el texto según el diccionario
            de Freeling y Wiktionary.
        """

    def calcular_feature(self, tweet):
        texto = tweet.texto
        texto = remover_hashtags(texto)
        texto = remover_usuarios(texto)
        oraciones = Freeling.procesar_texto(texto)
        tokens = list(itertools.chain(*oraciones))

        cant_palabras_oov = 0
        for token_freeling in tokens:
            if not token_freeling.tag.startswith('F') \
                    and not token_freeling.tag.startswith('Z') \
                    and not token_freeling.tag.startswith('W'):
                token = eliminar_underscores(token_freeling.token)
                if not Freeling.esta_en_diccionario(token) and not Wiktionary.pertenece(token):
                    cant_palabras_oov += 1

        if len(tokens) == 0:
            return 0
        else:
            return cant_palabras_oov / math.sqrt(len(tokens))
