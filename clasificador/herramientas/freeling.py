# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from contextlib import closing
import re
import itertools
import socket


patron_todo_espacios = re.compile(r'^\s*$', re.UNICODE)
patron_linea_freeling = re.compile(r'^(.*)\s(.*)\s(.*)\s(.*)', re.UNICODE)


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
        for linea in resultado.split('\n'):
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

        oraciones.append(oracion)

        return oraciones

    @staticmethod
    def analyzer_client(texto):
        resultado = Freeling.respuesta_socket_freeling(texto)
        while len(resultado) == 0 or resultado[0] == '/bin/sh: fork: Resource temporarily unavailable\n' \
                or resultado[0] == 'Server not ready?\n':
            print(resultado)
            print(len(texto), texto)
            print("En este loop")
            resultado = Freeling.respuesta_socket_freeling(texto)
        return resultado

    @staticmethod
    def respuesta_socket_freeling(texto):
        with closing(socket.socket(socket.AF_INET, socket.SOCK_STREAM)) as s:
            s.connect(('127.0.0.1', 55555))
            mensaje = (texto + '\0').encode('utf-8')
            s.send(mensaje)
            return s.recv(3000).decode('utf-8').strip()

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
