# coding=utf-8
from __future__ import absolute_import, unicode_literals

from clasificador.features.feature import Feature


def guiones_dialogo():
    return ['-', '—', '–', '―', '‒', '‐', '−', '­', '‑', '⁃', '֊', '˗', '⁻', '⏤', '─', '➖']
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
        for guion in guiones_dialogo():
            if tweet.texto.startswith(guion):
                return True
        return False
