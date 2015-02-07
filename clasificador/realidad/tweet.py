# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import HTMLParser  # import html.parser  # in python 3
import re

patron_retweet = re.compile(r'^RT @\w+: ', re.UNICODE)

patron_url = re.compile(
    r'(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)',
    re.IGNORECASE
)

patron_espacios_multiples = re.compile(r' +')

# Rodeo esta y otras regexes con paréntesis para poder referenciarlas enteras al hacer una sustitución en tweetenvivo.py
patron_hashtag = re.compile(r'(\B#\w+)', re.UNICODE)

patron_usuario = re.compile(r'(\B@\w+)', re.UNICODE)


def remover_retweet_si_hay(texto):
    return re.sub(patron_retweet, '', texto)


def remover_links(texto):
    return re.sub(patron_url, '', texto)


def remover_hashtags(texto):
    return re.sub(patron_hashtag, '', texto)


def remover_usuarios(texto):
    return re.sub(patron_usuario, '', texto)


def remover_espacios_multiples_y_strip(texto):
    return re.sub(patron_espacios_multiples, ' ', texto).strip()


class Tweet:
    def __init__(self):
        self.cuenta = ""
        self.es_chiste = False  # Si pertenece al subcorpus humor, aunque haya sido votado como no humor por la gente.
        self.es_humor = False
        self.evaluacion = False
        self.favoritos = 0
        self.id = 0
        self.retweets = 0
        self.seguidores = 0
        self.texto = ""
        self.texto_original = ""
        self.votos = 0
        self.votos_humor = 0
        self.promedio_de_humor = 0
        self.parecido_a_otro_con_distinto_humor = False

        self.features = {}

        self.oraciones = None
        self.tokens = None

    def preprocesar(self):
        self.texto_original = self.texto
        self.texto = HTMLParser.HTMLParser().unescape(self.texto)
        self.texto = remover_retweet_si_hay(self.texto)
        self.texto = remover_links(self.texto)
        self.texto = remover_espacios_multiples_y_strip(self.texto)

    def cantidad_links(self):
        return len(re.findall(patron_url, self.texto_original))

    def cantidad_hashtags(self):
        return len(re.findall(patron_hashtag, self.texto_original))

    def nombres_features_ordenadas(self):
        """Devuelve una lista de los nombres de las features ordenada según el nombre de las features."""
        return sorted(self.features.keys())

    def valores_features_ordenados(self):
        """Devuelve una lista de los valores de las features ordenada según el nombre de las features."""
        return [valor for (_, valor) in sorted(self.features.items())]

    def array_features(self):
        return self.valores_features_ordenados()
