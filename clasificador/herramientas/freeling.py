# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import re
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
            elif linea == '\n':  # FIXME: no está separando bien en oraciones.
                oraciones.append(oracion)
                oracion = []

        oraciones.append(oracion)

        return oraciones

    @staticmethod
    def analyzer_client_morfo(texto):
        return Freeling.analyzer_client(texto, puerto=11111)

    @staticmethod
    def analyzer_client(texto, puerto=55555):
        resultado = Freeling.respuesta_socket_freeling(texto, puerto=puerto)
        while len(resultado) == 0 or resultado[0] == "/bin/sh: fork: Resource temporarily unavailable\n" \
                or resultado[0] == "Server not ready?\n":
            print(resultado)
            print(len(texto), texto)
            print("En este loop")
            resultado = Freeling.respuesta_socket_freeling(texto, puerto=puerto)
        return resultado

    @staticmethod
    def respuesta_socket_freeling(texto, puerto):
        with AnalyzerClient() as client:
            client.connect(('127.0.0.1', puerto))
            client.send(texto)
            return client.recv(len(texto) * 10)

    @staticmethod
    def get_tokens_de_oraciones(oraciones):
        return list(itertools.chain(*oraciones))

    @staticmethod
    def esta_en_diccionario(texto):
        if patron_todo_espacios.match(texto):
            return True
        resultado = Freeling.analyzer_client_morfo(texto)
        return len(resultado) == 0 or resultado != texto


# DataType
class TokenFL:
    def __init__(self):
        self.token = ""
        self.tag = ""
        self.lemma = ""
        self.probabilidad = ""


MSG_FLUSH_BUFFER = 'FLUSH_BUFFER'
MSG_RESET_STATS = 'RESET_STATS'
MSG_SERVER_READY = 'FL-SERVER-READY'


class AnalyzerClient:
    def __init__(self):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __asegurar_servidor_pronto(self):
        assert self.recv(50) == MSG_SERVER_READY, "El servidor de Freeling debería haber respondido que está pronto"

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

    def recv(self, tam_buffer):
        resultado = self._socket.recv(tam_buffer).decode('utf-8')
        assert resultado.endswith('\0'), "El mensaje recibido del servidor de Freeling debería terminar en \\0"
        return resultado[:-1].strip()

    def send(self, mensaje):
        return self._socket.send((mensaje + '\0').encode('utf-8'))
