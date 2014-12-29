#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.persistencia import cargar_tweets
from clasificador.herramientas.utilclasificacion import cross_validation_y_reportar
from clasificador.herramientas.utils import filtrar_segun_votacion, get_stop_words
from experimentos.util import entrenar_y_evaluar


if __name__ == "__main__":
    corpus = cargar_tweets(cargar_features=False)

    filtrar_segun_votacion(corpus)

    features = [tweet.texto for tweet in corpus]
    clases = [tweet.es_humor for tweet in corpus]

    X_train, X_test, y_train, y_test = train_test_split(features, clases, test_size=0.20)

    clasificador = Pipeline([
        ('vect', CountVectorizer(
            stop_words=get_stop_words(),
            token_pattern=r'\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b',
        )),
        ('clf', MultinomialNB(alpha=0.01)),
    ])

    clasificador.fit(X_train, y_train)
    cross_validation_y_reportar(clasificador, features, clases, 5)
    entrenar_y_evaluar(clasificador, X_train, X_test, y_train, y_test)
