# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import math

import numpy
from sklearn import cross_validation, metrics


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


def get_features(tweets):
    assert len(tweets) > 0, "Deben haber tweets para obtener las features y las clases"

    largo_esperado_features = len(tweets[0].array_features())  # .shape[1]

    resultado = []
    for tweet in tweets:
        features_tweet = tweet.array_features()
        assert len(features_tweet) == largo_esperado_features, "Los tweets tienen distinta cantidad de features"
        resultado.append(features_tweet)

    return resultado  # vstack(resultado)


def get_clases(tweets):
    return numpy.array([tweet.es_humor for tweet in tweets], dtype=float)


def cross_validation_y_reportar(clasificador, features, clases, numero_particiones):
    print("Haciendo cross-validation...")
    puntajes = cross_validation.cross_val_score(clasificador, features, clases, cv=numero_particiones, verbose=True)
    # puntajes2 = cross_validation.cross_val_score(clasificador, features, clases, cv=numero_particiones, verbose=True,
    #                                             scoring=metrics.precision_recall_fscore_support)
    # print('Cross-validation:')
    print('')
    print("Acierto de cada partición:\t" + str(puntajes))
    promedio = puntajes.mean()
    delta = puntajes.std() * 1.96 / math.sqrt(numero_particiones)
    print("Intervalo de confianza 95%:\t{promedio:0.4f} (+/- {delta:0.4f}) --- [{inf:0.4f}, {sup:0.4f}]".format(
        promedio=promedio, delta=delta, inf=promedio - delta, sup=promedio + delta))
    print('')
    print('')


def matriz_de_confusion_y_reportar(_evaluacion, _clases_evaluacion, _clases_predecidas):
    _verdaderos_positivos = [_evaluacion[_i] for _i in range(len(_evaluacion)) if
                             _clases_predecidas[_i] and _clases_evaluacion[_i]]
    _falsos_positivos = [_evaluacion[_i] for _i in range(len(_evaluacion)) if
                         _clases_predecidas[_i] and not _clases_evaluacion[_i]]
    _falsos_negativos = [_evaluacion[_i] for _i in range(len(_evaluacion)) if
                         not _clases_predecidas[_i] and _clases_evaluacion[_i]]
    _verdaderos_negativos = [_evaluacion[_i] for _i in range(len(_evaluacion)) if
                             not _clases_predecidas[_i] and not _clases_evaluacion[_i]]

    # Reporte de estadísticas

    print(metrics.classification_report(_clases_evaluacion, _clases_predecidas, target_names=['N', 'P']))

    print("Acierto: " + str(metrics.accuracy_score(_clases_evaluacion, _clases_predecidas)))
    print('')

    matriz_de_confusion = metrics.confusion_matrix(_clases_evaluacion, _clases_predecidas, labels=[True, False])
    # Con 'labels' pido el orden para la matriz

    assert len(_verdaderos_positivos) == matriz_de_confusion[0][0]
    assert len(_falsos_negativos) == matriz_de_confusion[0][1]
    assert len(_falsos_positivos) == matriz_de_confusion[1][0]
    assert len(_verdaderos_negativos) == matriz_de_confusion[1][1]

    print("Matriz de confusión:")
    print('')
    print("\t\t(clasificados como)")
    print("\t\tP\tN")
    print("(son)\tP\t" + str(len(_verdaderos_positivos)) + '\t' + str(len(_falsos_negativos)))
    print("(son)\tN\t" + str(len(_falsos_positivos)) + '\t' + str(len(_verdaderos_negativos)))
    print('')

    return _verdaderos_positivos, _falsos_negativos, _falsos_positivos, _verdaderos_negativos
