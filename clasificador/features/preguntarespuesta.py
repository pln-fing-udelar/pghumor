# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re
import clasificador.features.dialogo

from clasificador.features.feature import Feature


def guiones_dialogo_re():
    guiones = ur"("
    for guion in clasificador.features.dialogo.guiones_dialogo():
        guiones += guion + ur"|"

    return guiones[:-1] + ur")"


patron = re.compile(ur'^(' + guiones_dialogo_re() + ur'\s*)?¿[^\?]+\?+[^¿\?]+$', re.UNICODE)


class PreguntaRespuesta(Feature):
    def __init__(self):
        super(PreguntaRespuesta, self).__init__()
        self.nombre = 'PreguntaRespuesta'
        self.descripcion = """
            Dice si es un formato pregunta - respuesta.
        """

    def calcular_feature(self, tweet):
        # TODO: hacer que mire cuántas oraciones de Freeling son
        tweet.features[self.nombre] = patron.search(tweet.texto) is not None
