from __future__ import absolute_import, division, unicode_literals

import abc


class Feature:
    __metaclass__ = abc.ABCMeta

    def __init__(self):
        self.nombre = ""
        self.descripcion = ""
        self.incluir = True

    @abc.abstractmethod
    def calcular_feature(self, tweet):
        """Calcula y devuelve el valor de la feature para el tweet"""
        raise NotImplementedError
