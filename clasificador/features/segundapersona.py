# -*- coding: utf-8 -*-
from __future__ import absolute_import

from clasificador.features.xpersona import XPersona


class SegundaPersona(XPersona):
    def __init__(self):
        super(SegundaPersona, self).__init__(2)
        self.nombre = "Segunda Persona"
        self.descripcion = """
            Mide si el texto está expresado en segunda segunda.
        """

# Hereda la funcion calcular feature de la clase X persona
