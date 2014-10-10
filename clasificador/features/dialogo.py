# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.feature import Feature


def guiones_dialogo():
    return [u'-', u'—', u'–', u'―', u'‒', u'‐', u'−', u'­', u'‑', u'⁃', u'֊', u'˗', u'⁻', u'⏤', u'─', u'➖']
    # Estos símbolos no son iguales; son distintos guiones (algunos son hyphen, otros dashes,
    # otros minus sign, viñetas, etc.)


class Dialogo(Feature):
    def __init__(self):
        super(Dialogo, self).__init__()
        self.nombre = "Dialogo"
        self.descripcion = """
            Mide si existe un diálogo en el tweet.
        """

    def calcular_feature(self, tweet):
        tweet.features[self.nombre] = False
        for guion in guiones_dialogo():
            if tweet.texto.startswith(guion):
                tweet.features[self.nombre] = True
                break
