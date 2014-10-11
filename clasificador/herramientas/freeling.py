# coding=utf-8
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
            # TODO: no debería ser siempre el texto original
            self.oraciones = Freeling.procesar_texto(tweet.texto_original)
            Freeling.cache[tweet.id] = self
        assert type(self.oraciones[0]) is list
        print type(self.oraciones[0]) is list
        assert self.oraciones != []
        self.tokens = Freeling.get_tokens_de_oraciones(self.oraciones)
        print type(self.oraciones[0]) is list

    @staticmethod
    def procesar_texto(texto):
        if re.search(r'^\s*$', texto) is not None:
            return []

        comando = "echo '" + clasificador.herramientas.utils.escapar(texto) + "' | analyzer_client 55555"
        resultado = clasificador.herramientas.utils.ejecutar_comando(comando)
        while len(resultado) == 0 or resultado[0] == '/bin/sh: fork: Resource temporarily unavailable\n' or resultado[
                0] == 'Server not ready?\n':
            resultado = clasificador.herramientas.utils.ejecutar_comando(comando)

        oraciones = []
        oracion = []
        for linea in resultado:
            matcheo = re.search(r'^(.*)\s(.*)\s(.*)\s(.*)\n', linea)
            if matcheo is not None:
                detalle = TokenFL()
                detalle.token = matcheo.group(1)
                detalle.lemma = matcheo.group(2)
                detalle.tag = matcheo.group(3)
                detalle.probabilidad = matcheo.group(4)

                oracion.append(detalle)
            elif linea == '\n':
                oraciones.append(oracion)
                oracion = []
        assert type(oraciones[0]) is list
        return oraciones

    @staticmethod
    def get_tokens_de_oraciones(oraciones):
        return list(itertools.chain(*oraciones))


# DataType
class TokenFL:
    def __init__(self):
        self.token = ""
        self.tag = ""
        self.lemma = ""
        self.probabilidad = ""
