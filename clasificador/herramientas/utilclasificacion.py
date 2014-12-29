# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import random

import numpy
from sklearn import cross_validation


def train_test_split_pro(corpus, **options):
    """Es como el de sklearn, pero como no deja saber qué tweets están en qué conjunto,
    hicimos este.
    # features_entrenamiento, features_evaluacion, clases_entrenamiento, clases_evaluacion
    # = train_test_split(features, clases, test_size=fraccion_evaluacion)
    """
    fraccion_evaluacion = options.pop('test_size', 0.25)

    elegir_fraccion = random.sample(range(len(corpus)), int(len(corpus) * fraccion_evaluacion))
    entrenamiento = [corpus[j] for j in range(len(corpus)) if j not in elegir_fraccion]
    evaluacion = [corpus[j] for j in elegir_fraccion]

    return entrenamiento, evaluacion


def features_clases_split(tweets):
    assert len(tweets) > 0, "Deben haber tweets para obtener las features y las clases"
    largo_esperado_features = len(tweets[0].valores_features_ordenados())
    features = []
    for tweet in tweets:
        features_tweet = tweet.valores_features_ordenados()
        assert len(features_tweet) == largo_esperado_features, "Los tweets tienen distinta cantidad de features"
        features.append(features_tweet)
    clases = numpy.array([tweet.es_humor for tweet in tweets], dtype=float)
    return features, clases


def cross_validation_y_reportar(clasificador, features, clases, numero_particiones):
    puntajes = cross_validation.cross_val_score(clasificador, features, clases, cv=numero_particiones, verbose=True)
    print('Cross-validation:')
    print('')
    print('Puntajes: ' + str(puntajes))
    print("Acierto: %0.4f (+/- %0.4f)" % (puntajes.mean(), puntajes.std() * 2))
    print('')
    print('')
