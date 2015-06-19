# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import math

from nltk.corpus import WordNetCorpusReader
from pkg_resources import resource_filename

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling
from clasificador.realidad.tweet import remover_hashtags, remover_usuarios
from clasificador.herramientas.persistencia import  guardar_feature

class Antonimos(Feature):
    def __init__(self):
        super(Antonimos, self).__init__()
        self.nombre = "Antonimos"
        self.descripcion = """
            Mide la cantidad de pares de antónimos presentes en el texto.
        """
        self.thread_safe = False  # Tiene problemas de concurrencia: https://github.com/nltk/nltk/issues/803
        self.wncr = WordNetCorpusReader(resource_filename('clasificador.recursos', 'wordnet_spa'), None)

    def calcular_feature(self, tweet):
        oraciones = Freeling.procesar_texto(remover_hashtags(remover_usuarios(tweet.texto)))
        tokens = Freeling.get_tokens_de_oraciones(oraciones)

        cant_antonimos = 0

        for token in tokens:
            antonimos = []
            for synset in self.wncr.synsets(token.lemma):
                for lemma in synset.lemmas():
                    antonimos += [lemma_antonimo.name() for lemma_antonimo in lemma.antonyms()]

            for otro_token in tokens:
                if otro_token.lemma in antonimos:
                    cant_antonimos += 1
                    break

        if len(tokens) == 0:
            return 0
        else:
            return cant_antonimos / math.sqrt(len(tokens)) / 2.0  # divido entre 2 para contar una vez cada par

    def calcular_feature_PRUEBA(self, tweet):
        oraciones = Freeling.procesar_texto(remover_hashtags(remover_usuarios(tweet.texto)))
        tokens = Freeling.get_tokens_de_oraciones(oraciones)

        cant_antonimos = 0

        for token in tokens:
            antonimos = []
            for synset in self.wncr.synsets(token.lemma):
                for lemma in synset.lemmas():
                    antonimos += [lemma_antonimo.name() for lemma_antonimo in lemma.antonyms()]

            for otro_token in tokens:
                if otro_token.lemma in antonimos:
                    cant_antonimos += 1
                    break

        if len(tokens) == 0:
            guardar_feature(tweet,self.nombre,0)
        else:
            guardar_feature(tweet,self.nombre,cant_antonimos / math.sqrt(len(tokens)) / 2.0) # divido entre 2 para contar una vez cada par
