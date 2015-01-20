# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import re
import socket


patron_todo_espacios = re.compile(r'^\s*$', re.UNICODE)
patron_linea_freeling = re.compile(r'^(.+)\s(.+)\s(.+)\s(.+)$', re.UNICODE)


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
        """Devuelve el resultado de analizar el texto con Freeling, pasando a minúsculas, sino Freeling toma como
        entidades con nombre a cualquier secuencia de palabras con la primer letra en mayúsculas de cada una,
        y los tweets en general tienen errores en las mayúsculas y minúsculas."""
        texto = texto.lower()

        if patron_todo_espacios.match(texto):
            return []

        resultado = Freeling.analyzer_client(texto)

        oraciones = []
        oracion = []
        for linea in resultado.split('\n'):
            matcheo = patron_linea_freeling.match(linea)
            if matcheo:
                token_freeling = TokenFL()
                token_freeling.token = matcheo.group(1)
                token_freeling.lemma = matcheo.group(2)
                token_freeling.tag = matcheo.group(3)
                token_freeling.probabilidad = matcheo.group(4)
                oracion.append(token_freeling)
            elif linea == '':
                oraciones.append(oracion)
                oracion = []

        if len(oracion) > 0:
            oraciones.append(oracion)

        return oraciones

    @staticmethod
    def analyzer_client(texto, puerto=55555):  # FIXME: no es pasado por minúsculas esta parte
        return Freeling.respuesta_socket_freeling(texto, puerto=puerto)

    @staticmethod
    def analyzer_client_morfo(texto):
        return Freeling.analyzer_client(texto, puerto=11111)

    @staticmethod
    def respuesta_socket_freeling(texto, puerto):
        with AnalyzerClient() as client:
            client.connect(('127.0.0.1', puerto))
            client.send(texto)
            return client.recv()

    @staticmethod
    def get_tokens_de_oraciones(oraciones):
        return list(itertools.chain(*oraciones))

    @staticmethod
    def esta_en_diccionario(texto):
        if patron_todo_espacios.match(texto):
            return True
        resultado = Freeling.analyzer_client_morfo(texto)
        return len(resultado) == 0 or resultado != texto  # TODO: si pongo en minúsculas lo otro, debo comparar bien acá


# DataType
class TokenFL:
    def __init__(self, token="", lemma="", tag="", probabilidad=""):
        self.token = token
        self.tag = tag
        self.lemma = lemma
        self.probabilidad = probabilidad

    def __eq__(self, other):
        return isinstance(other, TokenFL) and self.token == other.token and self.tag == other.tag \
               and self.lemma == other.lemma and self.probabilidad == other.probabilidad

    def __ne__(self, other):
        return not self.__eq__(other)


MSG_FLUSH_BUFFER = 'FLUSH_BUFFER'
MSG_RESET_STATS = 'RESET_STATS'
MSG_SERVER_READY = 'FL-SERVER-READY'


class AnalyzerClient:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __asegurar_servidor_pronto(self):
        assert self.recv() == MSG_SERVER_READY, "El servidor de Freeling debería haber respondido que está pronto"

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.send(MSG_FLUSH_BUFFER)
        self.__asegurar_servidor_pronto()
        self._socket.close()

    def connect(self, address):
        self._socket.connect(address)
        self.send(MSG_RESET_STATS)
        self.__asegurar_servidor_pronto()

    def recv(self):
        resultado = ""
        while True:
            resultado += self._socket.recv(4096).decode('utf-8')
            if resultado.endswith('\0'):
                break
        return resultado[:-1].strip()

    def send(self, mensaje):
        return self._socket.send((mensaje + '\0').encode('utf-8'))
