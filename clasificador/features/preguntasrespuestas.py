# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re

from clasificador.features.feature import Feature
from clasificador.features.preguntarespuesta import guiones_dialogo_re

patron = re.compile(ur'^((' + guiones_dialogo_re() + ur'\s*)?¿[^\?]+\?+[^¿\?]+)+$', re.UNICODE)


class PreguntasRespuestas(Feature):
    def __init__(self):
        super(PreguntasRespuestas, self).__init__()
        self.nombre = "PreguntasRespuestas"
        self.descripcion = """
            Dice si el tweet son varias preguntas y respuestas (pregunta - respuesta - pregunta - respuesta - ...).
        """

    def calcular_feature(self, tweet):
        return patron.search(tweet.texto) is not None
