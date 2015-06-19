# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import re

from clasificador.features.feature import Feature
from clasificador.features.dialogo import guiones_dialogo
from clasificador.herramientas.persistencia import  guardar_feature

def guion_dialogo_re():
    return r'(?:' + r'|'.join(guiones_dialogo()) + r')'


patron_pregunta_respuesta = re.compile(r"""
                    ¿+ [^\?]+ \?+ # pregunta
                    [^¿\?]* [\w\d] # respuesta
                    """, re.UNICODE | re.VERBOSE)


def cantidad_de_capturas_no_solapadas(_patron, _str):
    return _patron.subn('', _str)[1]


class PreguntasRespuestas(Feature):
    def __init__(self):
        super(PreguntasRespuestas, self).__init__()
        self.nombre = "PreguntasRespuestas"
        self.descripcion = """
            Dice la cantidad de preguntas seguidas de respuestas del tweet.
        """
        # Se basa en que el tweet es un texto corto. Si fuera más largo, la feature indicaría poco al agarrar
        # una pregunta cualquiera del texto; debería ser una pregunta al comienzo o al final tal vez.

    def calcular_feature(self, tweet):
        return cantidad_de_capturas_no_solapadas(patron_pregunta_respuesta, tweet.texto)

    def calcular_feature_PRUEBA(self, tweet):
        retorno = cantidad_de_capturas_no_solapadas(patron_pregunta_respuesta, tweet.texto)
        guardar_feature(tweet,self.nombre,retorno)