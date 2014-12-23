# coding=utf-8
from __future__ import absolute_import, unicode_literals

import math

from pkg_resources import resource_filename

from clasificador.features.feature import Feature
import clasificador.herramientas.define
from clasificador.herramientas.freeling import Freeling
import clasificador.herramientas.utils


class JergaSexual(Feature):
    def __init__(self):
        super(JergaSexual, self).__init__()
        self.nombre = "Jerga Sexual"
        self.descripcion = """
            Mide la cantidad de jerga sexual que contiene el texto.
        """
        self.palabrasSexuales = clasificador.herramientas.utils.obtener_diccionario(
            resource_filename('clasificador.recursos.diccionarios', 'DiccionarioSexual.txt'))

    def calcular_feature(self, tweet):
        tf = Freeling(tweet)
        cant_palabras_sexuales = 0
        for token in tf.tokens:
            if token.token in self.palabrasSexuales or token.lemma in self.palabrasSexuales:
                cant_palabras_sexuales += 1

        if len(tf.tokens) == 0:
            print("Error de tokens vacíos en " + self.nombre + ": ", tweet.texto)
            return 0
        else:
            return cant_palabras_sexuales / math.sqrt(len(tf.tokens))
