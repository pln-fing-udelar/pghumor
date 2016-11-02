#!/usr/bin/env python

from __future__ import print_function
import random

from clasificador.herramientas import freeling, persistencia

tweets = persistencia.cargar_tweets(cargar_features=False, agregar_sexuales=True)

for tweet in tweets:
    if tweet.es_humor:
        oraciones = freeling.Freeling.procesar_texto(tweet.texto)
        for oracion in oraciones:
            for token in oracion:
                if token.tag.startswith('V'):
                    print(token.token, token.tag, token.lemma, token.probabilidad)

        if random.random() < 0.01:
            break
