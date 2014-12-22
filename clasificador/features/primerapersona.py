# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from clasificador.features.npersona import NPersona


class PrimeraPersona(NPersona):
    def __init__(self):
        super(PrimeraPersona, self).__init__(1)
        self.nombre = "Primera Persona"
        self.descripcion = """
            Mide si el texto está expresado en primera persona.
        """

# Hereda la funcion calcular feature de la clase X persona
