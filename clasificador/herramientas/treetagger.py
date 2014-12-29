# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
import pipes
import re

import clasificador.herramientas.utils


class TreeTagger:
    cache = {}

    def __init__(self, tweet):
        if tweet.id not in TreeTagger.cache:
            self.tokens = TreeTagger.procesar_texto(tweet.texto_original)
            TreeTagger.cache[tweet.id] = self
        else:
            # Esta en cache
            self.tokens = TreeTagger.cache[tweet.id].tokens

    @staticmethod
    def procesar_texto(texto):
        command = 'echo ' + pipes.quote(texto) + ' | tree-tagger-spanish'
        resultado = clasificador.herramientas.utils.ejecutar_comando(command)
        tokens = []
        for line in resultado:
            matcheo = re.search(r'^(.*)\t(.*)\t(.*)\n', line)
            if matcheo:
                detalle = TokenTT()
                detalle.token = matcheo.group(1)
                detalle.tag = matcheo.group(2)
                detalle.lemma = matcheo.group(3)

                tokens.append(detalle)

        return tokens


# Datatype
class TokenTT:
    def __init__(self):
        self.token = ""
        self.tag = ""
        self.lemma = ""
