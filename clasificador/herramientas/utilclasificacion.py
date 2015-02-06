# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import random
import math

import numpy as np
from progress.bar import Bar
from sklearn import cross_validation, metrics

from clasificador.herramientas.define import SUFIJO_PROGRESS_BAR


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
    assert len(tweets) > 0, "Deberían haber tweets para obtener las features y las clases"

    largo_esperado_features = len(tweets[0].array_features())  # .shape[1]

    resultado = []
    for tweet in tweets:
        features_tweet = tweet.array_features()
        assert len(features_tweet) == largo_esperado_features, "Los tweets tienen distinta cantidad de features"
        resultado.append(features_tweet)

    return resultado  # vstack(resultado)


def get_clases(tweets):
    return np.array([tweet.es_humor for tweet in tweets], dtype=float)


def cross_validation_y_reportar(clasificador, features, clases, numero_particiones):
    skf = cross_validation.StratifiedKFold(clases, n_folds=numero_particiones)
    features = np.array(features)
    clases = np.array(clases)
    matrices = []
    precision_positivo_cross_validation = []
    precision_negativo_cross_validation = []
    recall_positivo_cross_validation = []
    recall_negativo_cross_validation = []
    f1score_positivo_cross_validation = []
    f1score_negativo_cross_validation = []
    accuracy_cross_validation = []
    diccionario_array_medidas = {
        'Recall positivo': recall_positivo_cross_validation,
        'Recall negativo': recall_negativo_cross_validation,
        'Precision positivo': precision_positivo_cross_validation,
        'Precision negativo': precision_negativo_cross_validation,
        'F1-score positivo': f1score_positivo_cross_validation,
        'F1-score negativo': f1score_negativo_cross_validation,
        'Acierto': accuracy_cross_validation,
    }
    bar = Bar("Realizando cross-validation", max=numero_particiones, suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)
    for train, test in skf:
        clasificador.fit(features[train], clases[train])
        y_pred = clasificador.predict(features[test])
        cm = metrics.confusion_matrix(clases[test], y_pred).flatten()
        matrices.append(cm)
        metricas = calcular_medidas(*cm)
        recall_positivo_cross_validation.append(metricas['recall_positivo'])
        recall_negativo_cross_validation.append(metricas['recall_negativo'])
        precision_positivo_cross_validation.append(metricas['precision_positivo'])
        precision_negativo_cross_validation.append(metricas['precision_negativo'])
        f1score_positivo_cross_validation.append(metricas['f1score_positivo'])
        f1score_negativo_cross_validation.append(metricas['f1score_negativo'])
        accuracy_cross_validation.append(metricas['accuracy'])
        bar.next()

    bar.finish()

    print("Resultados de cross-validation:")
    print('')
    mean = {}
    for key, puntajes in diccionario_array_medidas.iteritems():
        print(key + ":\t" + str(puntajes))
        promedio = np.mean(puntajes)
        mean[key] = promedio
        delta = np.std(puntajes) * 1.96 / math.sqrt(numero_particiones)
        print("Intervalo de confianza 95%:\t{promedio:0.4f} (+/- {delta:0.4f}) --- [{inf:0.4f}, {sup:0.4f}]".format(
            promedio=promedio, delta=delta, inf=promedio - delta, sup=promedio + delta))
        print('')

    # Matriz de cross-validation
    print("               precision      recall    f1-score\n")
    print("          N       {pn:0.4f}      {rn:0.4f}      {fn:0.4f}".format(pn=mean['Precision negativo'],
                                                                             rn=mean['Recall negativo'],
                                                                             fn=mean['F1-score negativo']))
    print("          P       {pp:0.4f}      {rp:0.4f}      {fp:0.4f}\n".format(pp=mean['Precision positivo'],
                                                                               rp=mean['Recall positivo'],
                                                                               fp=mean['F1-score positivo']))
    print("avg / total       {ap:0.4f}      {ar:0.4f}      {af:0.4f}".format(
        ap=(mean['Precision positivo'] + mean['Precision negativo']) / 2,
        ar=(mean['Recall positivo'] + mean['Recall negativo']) / 2,
        af=(mean['F1-score positivo'] + mean['F1-score negativo']) / 2),
    )

    print('')
    print('')


def calcular_medidas(tn, fp, fn, tp):
    """Dada la matriz de confusión desglozada, calcula todas las medidas."""
    metricas = {
        'precision_positivo': tp / (fp + tp),
        'precision_negativo': tn / (fn + tn),
        'recall_negativo': tn / (tn + fp),
        'recall_positivo': tp / (tp + fn),
        'accuracy': (tp + tn) / (tp + fp + tn + fn),
    }

    metricas['f1score_positivo'] = 2 * metricas['precision_positivo'] * metricas['recall_positivo'] / (
        metricas['precision_positivo'] + metricas['recall_positivo'])

    metricas['f1score_negativo'] = 2 * metricas['precision_negativo'] * metricas['recall_negativo'] / (
        metricas['precision_negativo'] + metricas['recall_negativo'])

    return metricas


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

    print("Acierto: " + str(metrics.accuracy_score(_clases_evaluacion, _clases_predecidas)))
    print('')
    tn = len(_verdaderos_negativos)
    fp = len(_falsos_positivos)
    fn = len(_falsos_negativos)
    tp = len(_verdaderos_positivos)

    # Matriz de cross-validation
    mean = calcular_medidas(tn, fp, fn, tp)
    print("               precision      recall    f1-score    support\n")
    print("          N       {pn:0.4f}      {rn:0.4f}      {fn:0.4f}      {sn}".format(pn=mean['precision_negativo'],
                                                                                       rn=mean['recall_negativo'],
                                                                                       fn=mean['f1score_negativo'],
                                                                                       sn=tn + fp))
    print("          P       {pp:0.4f}      {rp:0.4f}      {fp:0.4f}      {sp}\n".format(pp=mean['precision_positivo'],
                                                                                         rp=mean['recall_positivo'],
                                                                                         fp=mean['f1score_positivo'],
                                                                                         sp=tp + fn))
    print("avg / total       {ap:0.4f}      {ar:0.4f}      {af:0.4f}      {su}".format(
        ap=(mean['precision_positivo'] + mean['precision_negativo']) / 2,
        ar=(mean['recall_positivo'] + mean['recall_negativo']) / 2,
        af=(mean['f1score_positivo'] + mean['f1score_negativo']) / 2,
        su=tp + fp + tn + fn)
    )
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
