# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling
from clasificador.herramientas.google import Google
from clasificador.herramientas.utils import eliminar_underscores
from clasificador.realidad.tweet import *


class OOV(Feature):
    def __init__(self):
        super(OOV, self).__init__()
        self.nombre = "OOV"
        self.descripcion = """
            Mide la cantidad de palabras fuera del vocabulario que contiene el texto.
            Tiene en cuenta falta de ortografía, palabras no comunes, cosas como "holaaaaaa", etc.
            Éstas indican menos seriedad en el tweet. Por ejemplo, en una cuenta de CNN no ocurren este
            tipo de cosas. Por lo tanto, no interesa corregir las faltas para detectar la palabra verdadera.
        """
        self.thread_safe = False  # Sino Google bloquea las búsquedas.

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
                if not Freeling.esta_en_diccionario(token) and not Google.esta_en_google(token):
                    cant_palabras_oov += 1

        if len(tokens) == 0:
            return 0
        else:
            return cant_palabras_oov / math.sqrt(len(tokens))
