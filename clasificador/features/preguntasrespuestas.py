# coding=utf-8
from __future__ import absolute_import, unicode_literals

import re

from clasificador.features.feature import Feature
from clasificador.features.dialogo import guiones_dialogo


def guion_dialogo_re():
    return r"(?:" + r"|".join(guiones_dialogo()) + r")"


patron = re.compile(r"""
                    \s* """ + guion_dialogo_re() + r"""? \s* ¿+ [^\?]+ \?+ # pregunta
                    (?:[^¿\?]+ [^\s¿\?] [^¿\?]+) # respuesta
                    """, re.UNICODE | re.VERBOSE)


def cantidad_de_capturas_no_solapadas(_patron, _str):
    return _patron.subn('', _str)[1]


class PreguntasRespuestas(Feature):
    def __init__(self):
        super(PreguntasRespuestas, self).__init__()
        self.nombre = "PreguntasRespuestas"
        self.descripcion = """
            Dice la cantidad de pares de preguntas y respuestas del tweet bajo el formato:
            pregunta - respuesta - pregunta - respuesta - ...
        """

    def calcular_feature(self, tweet):
        return cantidad_de_capturas_no_solapadas(patron, tweet.texto)
