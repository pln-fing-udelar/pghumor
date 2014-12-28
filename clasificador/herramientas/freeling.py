# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import re
import itertools
import pipes

import clasificador.herramientas.utils


patron_todo_espacios = re.compile(r'^\s*$', re.UNICODE)
patron_linea_freeling = re.compile(r'^(.*)\s(.*)\s(.*)\s(.*)\n', re.UNICODE)


class Freeling:
    cache = {}

    def __init__(self, tweet):
        if tweet.id in Freeling.cache:
            self.oraciones = Freeling.cache[tweet.id].oraciones
        else:
            # TODO: no debería ser siempre el texto original
            self.oraciones = Freeling.procesar_texto(tweet.texto_original)
            Freeling.cache[tweet.id] = self
        self.tokens = Freeling.get_tokens_de_oraciones(self.oraciones)

    @staticmethod
    def procesar_texto(texto):
        # Se pasa a minúsculas, sino Freeling toma como entidades con nombre a cualquier secuencia de palabras con
        # la primer letra en mayúsculas de cada una.
        texto = texto.lower()

        if patron_todo_espacios.match(texto):
            return []

        resultado = Freeling.analyzer_client(texto)

        oraciones = []
        oracion = []
        for linea in resultado:
            matcheo = patron_linea_freeling.match(linea)
            if matcheo:
                detalle = TokenFL()
                detalle.token = matcheo.group(1)
                detalle.lemma = matcheo.group(2)
                detalle.tag = matcheo.group(3)
                detalle.probabilidad = matcheo.group(4)
                oracion.append(detalle)
            elif linea == '\n':
                oraciones.append(oracion)
                oracion = []

        return oraciones

    @staticmethod
    def analyzer_client(texto):
        comando = "echo " + pipes.quote(texto) + " | analyzer_client 55555"
        resultado = clasificador.herramientas.utils.ejecutar_comando(comando)
        while len(resultado) == 0 or resultado[0] == '/bin/sh: fork: Resource temporarily unavailable\n' \
                or resultado[0] == 'Server not ready?\n':
            print(resultado)
            print(len(texto), texto)
            print("En este loop")
            resultado = clasificador.herramientas.utils.ejecutar_comando(comando)
        return resultado

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
