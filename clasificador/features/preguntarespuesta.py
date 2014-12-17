# -*- coding: utf-8 -*-
from __future__ import absolute_import
import re

import clasificador.features.dialogo
from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling


def guion_dialogo_re():
    guiones = ur"("
    for guion in clasificador.features.dialogo.guiones_dialogo():
        guiones += guion + ur"|"

    return guiones[:-1] + ur")"


patron = re.compile(ur'^(' + guion_dialogo_re() + ur'\s*)?¿[^\?]+\?+[^¿\?]+$', re.UNICODE)


class PreguntaRespuesta(Feature):
    def __init__(self):
        super(PreguntaRespuesta, self).__init__()
        self.nombre = "PreguntaRespuesta"
        self.descripcion = """
            Dice si es el tweet tiene formato pregunta - respuesta.
        """

    def calcular_feature(self, tweet):
        freeling = Freeling(tweet)
        return len(freeling.oraciones) == 2 and freeling.oraciones[0][-1].tag == "Fit"
        # patron.search(tweet.texto) is not None
