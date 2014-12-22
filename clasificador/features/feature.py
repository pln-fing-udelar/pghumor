from __future__ import absolute_import, unicode_literals

import abc


class Feature:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.nombre = ""
        self.descripcion = ""

    @abc.abstractmethod
    def calcular_feature(self, tweet):
        """Calcula y devuelve el valor de la feature para el tweet"""
        return
