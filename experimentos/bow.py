#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, FeatureUnion

from experimentos.TweetToText import TweetToText
from experimentos.TweetsToFeatures import TweetsToFeatures


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.persistencia import cargar_tweets
from clasificador.herramientas.utilclasificacion import get_clases, \
    matriz_de_confusion_y_reportar, train_test_split_pro
from clasificador.herramientas.utils import filtrar_segun_votacion, get_stop_words

c = CountVectorizer()

if __name__ == "__main__":
    corpus = cargar_tweets(cargar_features=True)
    print('')
    print('')

    print("Filtrando y corrigiendo según la votación...")
    filtrar_segun_votacion(corpus)

    print("Separando en entrenamiento y evaluación...")
    entrenamiento, evaluacion = train_test_split_pro(corpus, test_size=0.2)

    print("Separando tweets en features y clases...")
    X = [tweet for tweet in corpus]
    y = get_clases(corpus)

    X_train = [tweet for tweet in entrenamiento]
    X_test = [tweet for tweet in evaluacion]

    y_train = get_clases(entrenamiento)
    y_test = get_clases(evaluacion)

    feature_union = FeatureUnion([
        ('vectorizer_bow', Pipeline([
            ('tweet_to_text', TweetToText()),
            ('vectorizer', CountVectorizer(
                strip_accents='ascii',
                stop_words=get_stop_words(),
                token_pattern=r'\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b',
            ))])
        ),
        ('features_tweets', TweetsToFeatures())

    ])

    clasificador = Pipeline([
        ('features', feature_union),
        # ('scaler', preprocessing.StandardScaler()),
        # ('features_tweets', TweetsToFeatures()),
        ('clf', MultinomialNB(alpha=0.01)),  # alpha=0.01
    ])

    print('')
    print('')

    # cross_validation_y_reportar(clasificador, X, y, 5)

    print("Entrenando clasificador...")
    clasificador.fit(X_train, y_train)

    print("Evaluando clasificador...")
    print('')
    y_pred = clasificador.predict(X_test)

    verdaderos_positivos, falsos_negativos, falsos_positivos, verdaderos_negativos = matriz_de_confusion_y_reportar(
        evaluacion, y_test, y_pred)
