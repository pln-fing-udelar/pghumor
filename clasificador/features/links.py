# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from clasificador.features.feature import Feature
from clasificador.herramientas.persistencia import  guardar_feature

class Links(Feature):
    def __init__(self):
        super(Links, self).__init__()
        self.nombre = "Links"
        self.descripcion = """
            Cuenta la cantidad de links.
        """

    def calcular_feature(self, tweet):
        return tweet.cantidad_links()

    def calcular_feature_PRUEBA(self, tweet):
        retorno = tweet.cantidad_links()
        guardar_feature(tweet,self.nombre,retorno)
