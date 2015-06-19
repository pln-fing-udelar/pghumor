# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from clasificador.features.feature import Feature
from clasificador.herramientas.persistencia import  guardar_feature

class Hashtags(Feature):
    def __init__(self):
        super(Hashtags, self).__init__()
        self.nombre = "Hashtags"
        self.descripcion = """
            Cuenta la cantidad de hashtags.
        """

    def calcular_feature(self, tweet):
        return tweet.cantidad_hashtags()

    def calcular_feature_PRUEBA(self, tweet):
        retorno = tweet.cantidad_hashtags()
        guardar_feature(tweet,self.nombre,retorno)