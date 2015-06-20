# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import abc

from clasificador.herramientas.persistencia import guardar_feature


class Feature:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.nombre = ""
        self.descripcion = ""
        self.incluir = True
        self.thread_safe = True

    @abc.abstractmethod
    def calcular_feature(self, tweet):
        """Calcula y devuelve el valor de la feature para el tweet"""
        raise NotImplementedError

    def calcular_feature_prueba(self, tweet):
        """Calcula y guarda el valor de la feature para el tweet"""
        guardar_feature(tweet, self.nombre, self.calcular_feature(tweet))

    def calcular_feature_prueba_tweets(self, tweets):
        """Calcula y guarda el valor de la feature para todos los tweets"""
        for tweet in tweets:
            self.calcular_feature_prueba(tweet)
