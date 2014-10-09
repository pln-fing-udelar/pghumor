from __future__ import absolute_import

import re
import itertools

import clasificador.herramientas.utils


class Freeling:
    cache = {}

    def __init__(self, tweet):
        if tweet.id in Freeling.cache:
            self.oraciones = Freeling.cache[tweet.id].tokens
        else:
            self.oraciones = Freeling.procesar_texto(tweet.texto_original)
            Freeling.cache[tweet.id] = self
        self.tokens = itertools.chain(*self.oraciones)

    @staticmethod
    def procesar_texto(texto):
        if re.search(r'^\s*$', texto) is not None:
            return []

        command = 'echo "' + clasificador.herramientas.utils.escapar(texto) + '" | analyzer_client 55555'
        resultado = clasificador.herramientas.utils.ejecutar_comando(command)
        while (len(resultado) == 0) or (
                (len(resultado) > 0) and resultado[0] == '/bin/sh: fork: Resource temporarily unavailable\n' or
                resultado[0] == 'Server not ready?\n'):
            resultado = clasificador.herramientas.utils.ejecutar_comando(command)

        oraciones = []
        oracion = []
        for line in resultado:
            matcheo = re.search(r'^(.*)\s(.*)\s(.*)\s(.*)\n', line)
            if matcheo is not None:
                detalle = TokenFL()
                detalle.token = matcheo.group(1)
                detalle.lemma = matcheo.group(2)
                detalle.tag = matcheo.group(3)
                detalle.probabilidad = matcheo.group(4)
                oracion.append(detalle)
            elif line == '\n':
                oraciones.append(oracion)
                oracion = []
        return oraciones


# DataType
class TokenFL:
    def __init__(self):
        self.token = ""
        self.tag = ""
        self.lemma = ""
        self.probabilidad = ""
