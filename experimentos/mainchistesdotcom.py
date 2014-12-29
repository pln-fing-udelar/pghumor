#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from sklearn.cross_validation import train_test_split
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from experimentos.persistencia import *
from experimentos.util import get_stop_words


if __name__ == "__main__":
    chistes = cargar_chistes()

    noticias = fetch_20newsgroups(subset='all')

    features = [chiste.texto for chiste in chistes]
    clases = [chiste.es_humor for chiste in chistes]

    X_train, X_test, y_train, y_test = train_test_split(features, clases, test_size=0.0)

    clasificador = Pipeline([
        ('vect', TfidfVectorizer(
            stop_words=get_stop_words(),
            token_pattern=r'\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b',
        )),
        ('clf', MultinomialNB(alpha=0.01)),
    ])

    clasificador.fit(X_train, y_train)
    # cross_validation_y_reportar(clasificador, features, clases, 5)
    # entrenar_y_evaluar(clasificador, X_train, X_test, y_train, y_test)

    tweets = cargar_tweets()

    tweets_humor = [chiste for chiste in tweets if chiste.es_humor]

    for tweet in tweets_humor:
        print(tweet.texto)
        result = clasificador.predict([tweet.texto])
        print("El resultado es " + result[0])
        sys.stdin.readline()
