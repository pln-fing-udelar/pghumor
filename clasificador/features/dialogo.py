# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from clasificador.features.feature import Feature


def guiones_dialogo():
    """Devuelve una lista de símbolos de diálogo posibles. Parecen todos iguales, pero son
    distintos (algunos son hyphen, otros dashes, otros minus sign, viñetas, etc.)"""
    return ['-', '—', '–', '―', '‒', '‐', '−', '­', '‑', '⁃', '֊', '˗', '⁻', '⏤', '─', '➖']


class Dialogo(Feature):
    def __init__(self):
        super(Dialogo, self).__init__()
        self.nombre = "Dialogo"
        self.descripcion = """
            Mide si existe un diálogo en el tweet.
        """

    def calcular_feature(self, tweet):
        for guion in guiones_dialogo():
            if tweet.texto.startswith(guion):
                return 1
        return 0
