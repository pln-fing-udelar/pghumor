# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
import random
import math

import numpy as np
from progress.bar import IncrementalBar
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
    entrenamiento = [corpus[i] for i in range(len(corpus)) if i not in elegir_fraccion]
    evaluacion = [corpus[i] for i in elegir_fraccion]

    return entrenamiento, evaluacion


def get_features(tweets):
    assert len(tweets) > 0, "Deberían haber tweets para obtener las features y las clases"

    largo_esperado_features = len(tweets[0].array_features())

    resultado = []
    for tweet in tweets:
        features_tweet = tweet.array_features()
        assert len(features_tweet) == largo_esperado_features, "Los tweets tienen distinta cantidad de features"
        resultado.append(features_tweet)

    return resultado


def get_clases(tweets):
    return np.array([tweet.es_humor for tweet in tweets], dtype=float)


def imprimir_matriz_metricas(pn, rn, fn, pp, rp, fp):
    print("               precision      recall    f1-score\n")
    print("     No humor     {pn:0.4f}      {rn:0.4f}      {fn:0.4f}".format(pn=pn,
                                                                             rn=rn,
                                                                             fn=fn))
    print("     Humor        {pp:0.4f}      {rp:0.4f}      {fp:0.4f}\n".format(pp=pp,
                                                                               rp=rp,
                                                                               fp=fp))
    print("avg / total       {ap:0.4f}      {ar:0.4f}      {af:0.4f}".format(
        ap=(pn + pp) / 2,
        ar=(rp + rn) / 2,
        af=(fp + fn) / 2,
    ))


def cross_validation_y_reportar(clasificador, features, clases, numero_particiones):
    skf = cross_validation.StratifiedKFold(clases, n_folds=numero_particiones)
    features = np.array(features)
    clases = np.array(clases)
    matrices = []
    medidas = defaultdict(list)

    bar = IncrementalBar("Realizando cross-validation\t", max=numero_particiones, suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)
    for entrenamiento, evaluacion in skf:
        clasificador.fit(features[entrenamiento], clases[entrenamiento])
        clases_predecidas = clasificador.predict(features[evaluacion])
        matriz_de_confusion = metrics.confusion_matrix(clases[evaluacion], clases_predecidas).flatten()
        matrices.append(matriz_de_confusion)
        for medida, valor_medida in calcular_medidas(*matriz_de_confusion).items():
            medidas[medida].append(valor_medida)
        bar.next()
    bar.finish()

    promedios = {}

    print('')
    print("Resultados de cross-validation:")
    print('')
    for medida, valor_medida in medidas.items():
        print("\t{medida: >18s}:\t{valor_medida}".format(medida=medida, valor_medida=valor_medida))
        promedio = np.mean(valor_medida)
        promedios[medida] = promedio
        delta = np.std(valor_medida) * 1.96 / math.sqrt(numero_particiones)
        print("Intervalo de confianza 95%:\t{promedio:0.4f} ± {delta:0.4f} --- [{inf:0.4f}, {sup:0.4f}]".format(
            promedio=promedio, delta=delta, inf=promedio - delta, sup=promedio + delta))
        print('')

    imprimir_matriz_metricas(
        promedios['Precision No humor'],
        promedios['Recall No humor'],
        promedios['F1-score No humor'],
        promedios['Precision Humor'],
        promedios['Recall Humor'],
        promedios['F1-score Humor'],
    )

    print('')
    print('')
    print('')


def calcular_medidas(tn, fp, fn, tp):
    """Dada la matriz de confusión desglozada, calcula todas las medidas."""
    return {
        'Precision No humor': tn / (tn + fn),
        'Recall No humor': tn / (tn + fp),
        'F1-score No humor': tn / (tn + (fp + fn) / 2),
        'Precision Humor': tp / (tp + fp),
        'Recall Humor': tp / (tp + fn),
        'F1-score Humor': tp / (tp + (fp + fn) / 2),
        'Acierto': (tp + tn) / (tp + fp + tn + fn),
    }


def reportar_metricas_ponderadas(verdaderos_negativos, falsos_positivos, falsos_negativos, verdaderos_positivos):
    tp = sum(tweet.promedio_de_humor for tweet in verdaderos_positivos)
    fn = sum(tweet.promedio_de_humor for tweet in falsos_negativos)

    prom_tn = sum(tweet.promedio_de_humor for tweet in verdaderos_negativos) / len(verdaderos_negativos)
    prom_fp = sum(tweet.promedio_de_humor for tweet in falsos_positivos) / len(falsos_positivos)
    prom_tp = sum(tweet.promedio_de_humor for tweet in verdaderos_positivos) / len(verdaderos_positivos)
    prom_fn = sum(tweet.promedio_de_humor for tweet in falsos_negativos) / len(falsos_negativos)

    recall_positivo = tp / (tp + fn)

    return recall_positivo, prom_tn, prom_fp, prom_tp, prom_fn


def matriz_de_confusion_y_reportar(evaluacion, clases_evaluacion, clases_predecidas, medidas_ponderadas):
    verdaderos_positivos = [evaluacion[_i] for _i in range(len(evaluacion)) if
                            clases_predecidas[_i] and clases_evaluacion[_i]]
    falsos_positivos = [evaluacion[_i] for _i in range(len(evaluacion)) if
                        clases_predecidas[_i] and not clases_evaluacion[_i]]
    falsos_negativos = [evaluacion[_i] for _i in range(len(evaluacion)) if
                        not clases_predecidas[_i] and clases_evaluacion[_i]]
    verdaderos_negativos = [evaluacion[_i] for _i in range(len(evaluacion)) if
                            not clases_predecidas[_i] and not clases_evaluacion[_i]]

    if medidas_ponderadas:
        print('')
        print("Reportando medidas ponderadas")
        recall_positivo, prom_tn, prom_fp, prom_tp, prom_fn = reportar_metricas_ponderadas(verdaderos_negativos,
                                                                                           falsos_positivos,
                                                                                           falsos_negativos,
                                                                                           verdaderos_positivos)
        print("Recall positivo: " + unicode(recall_positivo))
        print('')
        print("Matriz de confusión de promedio de humor:")
        print('')
        print("\t\t\t(clasificados como)")
        print("\t\t\tHumor\t\tNo humor")
        print("(son)\tHumor\t\t{tp:0.4f}\t\t{fn:0.4f}".format(tp=prom_tp, fn=prom_fn))
        print("(son)\tNo humor\t{fp:0.4f}\t\t{tn:0.4f}".format(fp=prom_fp, tn=prom_tn))
        print('')
        print('')

    # Reporte de estadísticas
    print("Acierto: {acierto:0.4f}".format(acierto=metrics.accuracy_score(clases_evaluacion, clases_predecidas)))
    print('')
    tn = len(verdaderos_negativos)
    fp = len(falsos_positivos)
    fn = len(falsos_negativos)
    tp = len(verdaderos_positivos)

    # Matriz de cross-validation
    promedios = calcular_medidas(tn, fp, fn, tp)
    print("               precision      recall    f1-score    support\n")
    print("     No humor     {pn:0.4f}      {rn:0.4f}      {fn:0.4f}      {sn}".format(
        pn=promedios['Precision No humor'], rn=promedios['Recall No humor'], fn=promedios['F1-score No humor'],
        sn=tn + fp))
    print("     Humor        {pp:0.4f}      {rp:0.4f}      {fp:0.4f}      {sp}\n".format(
        pp=promedios['Precision Humor'], rp=promedios['Recall Humor'], fp=promedios['F1-score Humor'], sp=tp + fn))
    print("avg / total       {ap:0.4f}      {ar:0.4f}      {af:0.4f}      {su}".format(
        ap=(promedios['Precision Humor'] + promedios['Precision No humor']) / 2,
        ar=(promedios['Recall Humor'] + promedios['Recall No humor']) / 2,
        af=(promedios['F1-score Humor'] + promedios['F1-score No humor']) / 2,
        su=tp + fp + tn + fn
    ))

    print('')

    matriz_de_confusion = metrics.confusion_matrix(clases_evaluacion, clases_predecidas, labels=[True, False])
    # Con 'labels' pido el orden para la matriz.

    assert len(verdaderos_positivos) == matriz_de_confusion[0][0]
    assert len(falsos_negativos) == matriz_de_confusion[0][1]
    assert len(falsos_positivos) == matriz_de_confusion[1][0]
    assert len(verdaderos_negativos) == matriz_de_confusion[1][1]

    print("Matriz de confusión:")
    print('')
    print("\t\t\t(clasificados como)")
    print("\t\t\tHumor\tNo humor")
    print("(son)\tHumor\t\t{vp: >d}\t{fn: >d}".format(vp=len(verdaderos_positivos), fn=len(falsos_negativos)))
    print("(son)\tNo humor\t{fp: >d}\t{vn: >d}".format(fp=len(falsos_positivos), vn=len(verdaderos_negativos)))
    print('')

    return verdaderos_positivos, falsos_negativos, falsos_positivos, verdaderos_negativos
