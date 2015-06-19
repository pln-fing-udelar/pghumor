# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling
from clasificador.herramientas.utils import eliminar_underscores
from clasificador.realidad.tweet import *

CARACTERES_ESPANOL = 255

patron_todo_espacios = re.compile(r'^\s*$', re.UNICODE)


def contiene_caracteres_no_espanoles(texto):
    return any(ord(c) > CARACTERES_ESPANOL for c in texto)


class OOV(Feature):
    def __init__(self):
        super(OOV, self).__init__()
        self.nombre = "Palabras no españolas"
        self.descripcion = """
            Cuenta la cantidad de palabras que contienen caracteres no españoles en el tweet.
        """
        self.thread_safe = False  # Sino Google bloquea las búsquedas.

    def calcular_feature(self, tweet):
        texto = tweet.texto
        texto = remover_hashtags(texto)
        texto = remover_usuarios(texto)
        oraciones = Freeling.procesar_texto(texto)
        tokens = list(itertools.chain(*oraciones))

        cant_palabras_no_espanolas = 0
        for token_freeling in tokens:
            token = eliminar_underscores(token_freeling.token)
            if len(token) >= 3 and contiene_caracteres_no_espanoles(token):
                cant_palabras_no_espanolas += 1

        if len(tokens) == 0:
            return 0
        else:
            return cant_palabras_no_espanolas / math.sqrt(len(tokens))
