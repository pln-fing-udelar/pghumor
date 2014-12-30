#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.persistencia import cargar_tweets
from clasificador.herramientas.utilclasificacion import cross_validation_y_reportar, get_clases, \
    matriz_de_confusion_y_reportar, train_test_split_pro
from clasificador.herramientas.utils import filtrar_segun_votacion, get_stop_words


if __name__ == "__main__":
    corpus = cargar_tweets(cargar_features=False)
    print('')
    print('')

    print("Filtrando y corrigiendo según la votación...")
    filtrar_segun_votacion(corpus)

    print("Separando en entrenamiento y evaluación...")
    entrenamiento, evaluacion = train_test_split_pro(corpus, test_size=0.2)

    print("Separando tweets en features y clases...")
    X = [tweet.texto for tweet in corpus]
    y = get_clases(corpus)

    X_train = [tweet.texto for tweet in entrenamiento]
    X_test = [tweet.texto for tweet in evaluacion]

    y_train = get_clases(entrenamiento)
    y_test = get_clases(evaluacion)

    clasificador = Pipeline([
        ('vect', CountVectorizer(
            stop_words=get_stop_words(),
            token_pattern=r'\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b',
        )),
        ('clf', MultinomialNB(alpha=0.01)),
    ])

    print('')
    print('')

    cross_validation_y_reportar(clasificador, X, y, 5)

    print("Entrenando clasificador...")
    clasificador.fit(X_train, y_train)
    print("Evaluando clasificador...")
    y_pred = clasificador.predict(X_test)
    print('')

    verdaderos_positivos, falsos_negativos, falsos_positivos, verdaderos_negativos = matriz_de_confusion_y_reportar(
        evaluacion, y_test, y_pred)
