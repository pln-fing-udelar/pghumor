# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re

from clasificador.features.feature import Feature

patron = re.compile(ur'^(((-|—)\s*)?¿[^\?]+\?+[^¿\?]+)+$', re.UNICODE)


class PreguntasRespuestas(Feature):
    def __init__(self):
        super(PreguntasRespuestas, self).__init__()
        self.nombre = "PreguntasRespuestas"
        self.descripcion = """
            Mide si el tweet son varias preguntas y respuestas (pregunta - respuesta - pregunta - respuesta - ...)
        """

    def calcular_feature(self, tweet):
        tweet.features[self.nombre] = patron.search(tweet.texto) is not None
