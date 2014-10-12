# -*- coding: utf-8 -*-
from __future__ import absolute_import

import math

from pkg_resources import resource_filename

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import *


class PalabrasClave(Feature):
    def __init__(self):
        super(PalabrasClave, self).__init__()
        self.nombre = "Palabras Claves"
        self.descripcion = """
            Mide la cantidad de palabras clave mencionadas en el texto.
        """
        self.palabrasAnimales = clasificador.herramientas.utils.obtener_diccionario(
            resource_filename('clasificador.recursos.diccionarios', 'DiccionarioFrecuentes.txt'))

    def calcular_feature(self, tweet):
        tf = Freeling(tweet)
        cant_palabras_claves = 0
        for token in tf.tokens:
            if (token.token in self.palabrasAnimales) or (token.lemma in self.palabrasAnimales):
                cant_palabras_claves += 1

        if len(tf.tokens) == 0:
            print("Error de tokens vacíos en " + self.nombre + ": ", tweet.texto)
            return 0
        else:
            return cant_palabras_claves / math.sqrt(len(tf.tokens))
