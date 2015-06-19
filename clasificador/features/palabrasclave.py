# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import math

from pkg_resources import resource_filename

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import *
import clasificador.herramientas.utils
from clasificador.herramientas.persistencia import  guardar_feature

class PalabrasClave(Feature):
    def __init__(self):
        super(PalabrasClave, self).__init__()
        self.nombre = "Palabras Claves"
        self.descripcion = """
            Mide la cantidad de palabras clave mencionadas en el texto.
        """
        self.palabrasAnimales = clasificador.herramientas.utils.obtener_diccionario(
            resource_filename('clasificador.recursos.diccionarios', 'frecuentes.dic'))

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


    def calcular_feature_PRUEBA(self, tweet):
        tf = Freeling(tweet)
        cant_palabras_claves = 0
        for token in tf.tokens:
            if (token.token in self.palabrasAnimales) or (token.lemma in self.palabrasAnimales):
                cant_palabras_claves += 1

        if len(tf.tokens) == 0:
            print("Error de tokens vacíos en " + self.nombre + ": ", tweet.texto)
            retorno = 0
        else:
            retorno = cant_palabras_claves / math.sqrt(len(tf.tokens))

        guardar_feature(tweet,self.nombre,retorno)
