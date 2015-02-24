# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
import random
import math

import numpy as np
from progress.bar import IncrementalBar
from sklearn import cross_validation, metrics

from clasificador.herramientas.define import SUFIJO_PROGRESS_BAR
from clasificador.herramientas.utils import entropia


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
    print("               precision      recall    f1-score")
    print('')
    print("     No humor     {pn:0.4f}      {rn:0.4f}      {fn:0.4f}".format(pn=pn,
                                                                             rn=rn,
                                                                             fn=fn))
    print("     Humor        {pp:0.4f}      {rp:0.4f}      {fp:0.4f}".format(pp=pp,
                                                                             rp=rp,
                                                                             fp=fp))
    print('')
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


def metricas_ponderadas_segun_concordancia(verdaderos_negativos, falsos_positivos, falsos_negativos,
                                           verdaderos_positivos):
    tn = sum(1 - entropia(tweet.votos_humor / tweet.votos) if tweet.votos > 0 else 1 for tweet in verdaderos_negativos)
    fp = sum(1 - entropia(tweet.votos_humor / tweet.votos) if tweet.votos > 0 else 1 for tweet in falsos_positivos)
    fn = sum(1 - entropia(tweet.votos_humor / tweet.votos) if tweet.votos > 0 else 1 for tweet in falsos_negativos)
    tp = sum(1 - entropia(tweet.votos_humor / tweet.votos) if tweet.votos > 0 else 1 for tweet in verdaderos_positivos)
    return tn, fp, fn, tp


def metricas_ponderadas_segun_humor(verdaderos_negativos, falsos_positivos, falsos_negativos, verdaderos_positivos):
    # Nota if tweet.es_chiste en tp y fn es siempre verdadero. Se prioriza claridad
    tp_suma_ph = sum(tweet.promedio_de_humor for tweet in verdaderos_positivos if tweet.es_chiste)
    fn_suma_ph = sum(tweet.promedio_de_humor for tweet in falsos_negativos if tweet.es_chiste)
    tn_suma_ph = sum(tweet.promedio_de_humor for tweet in verdaderos_negativos if tweet.es_chiste)
    fp_suma_ph = sum(tweet.promedio_de_humor for tweet in falsos_positivos if tweet.es_chiste)

    prom_tn = tn_suma_ph / len([tweet for tweet in verdaderos_negativos if tweet.es_chiste])
    prom_fp = fp_suma_ph / len([tweet for tweet in falsos_positivos if tweet.es_chiste])
    prom_tp = tp_suma_ph / len([tweet for tweet in verdaderos_positivos if tweet.es_chiste])
    prom_fn = fn_suma_ph / len([tweet for tweet in falsos_negativos if tweet.es_chiste])

    recall_positivo = tp_suma_ph / (tp_suma_ph + fn_suma_ph)

    return recall_positivo, prom_tn, prom_fp, prom_tp, prom_fn


def mostrar_medidas_ponderadas(evaluacion, clases_evaluacion, clases_predecidas):
    verdaderos_positivos, falsos_positivos, falsos_negativos, verdaderos_negativos = \
        calcular_verdaderos_falsos_positivos_negativos(evaluacion, clases_evaluacion, clases_predecidas)

    recall_positivo, prom_tn, prom_fp, prom_tp, prom_fn = metricas_ponderadas_segun_humor(verdaderos_negativos,
                                                                                 falsos_positivos,
                                                                                 falsos_negativos,
                                                                                 verdaderos_positivos)

    print("El recall humoristico ponderado es: {recall:0.4f}".format(recall=recall_positivo))
    print("")
    print("Matriz de confución mostrando el promedio de humor:")
    print("")
    imprimir_matriz_de_confucion(prom_tp, prom_fp, prom_tn, prom_fn)
    print("")


def calcular_verdaderos_falsos_positivos_negativos(evaluacion, clases_evaluacion, clases_predecidas):
    verdaderos_positivos = [evaluacion[i] for i in range(len(evaluacion)) if
                            clases_predecidas[i] and clases_evaluacion[i]]
    falsos_positivos = [evaluacion[i] for i in range(len(evaluacion)) if
                        clases_predecidas[i] and not clases_evaluacion[i]]
    falsos_negativos = [evaluacion[i] for i in range(len(evaluacion)) if
                        not clases_predecidas[i] and clases_evaluacion[i]]
    verdaderos_negativos = [evaluacion[i] for i in range(len(evaluacion)) if
                            not clases_predecidas[i] and not clases_evaluacion[i]]

    return verdaderos_positivos, falsos_positivos, falsos_negativos, verdaderos_negativos


def matriz_de_confusion_y_reportar(evaluacion, clases_evaluacion, clases_predecidas, medidas_ponderadas=""):

    verdaderos_positivos, falsos_positivos, falsos_negativos, verdaderos_negativos = \
        calcular_verdaderos_falsos_positivos_negativos(evaluacion, clases_evaluacion, clases_predecidas)

    if medidas_ponderadas == "concordancia":
        tn, fp, fn, tp = metricas_ponderadas_segun_concordancia(verdaderos_negativos, falsos_positivos,
                                                                falsos_negativos, verdaderos_positivos)
    else:
        tn = len(verdaderos_negativos)
        fp = len(falsos_positivos)
        fn = len(falsos_negativos)
        tp = len(verdaderos_positivos)

    promedios = calcular_medidas(tn, fp, fn, tp)

    if medidas_ponderadas != "":
        print('')
        print("Medidas ponderadas según {criterio}:".format(criterio=medidas_ponderadas))

    print("Acierto: {acierto:0.4f}".format(acierto=promedios['Acierto']))
    print('')
    tn = len(verdaderos_negativos)
    fp = len(falsos_positivos)
    fn = len(falsos_negativos)
    tp = len(verdaderos_positivos)

    # Matriz de cross-validation
    print("               precision      recall    f1-score    support")
    print('')
    print("     No humor     {pn:0.4f}      {rn:0.4f}      {fn:0.4f}      {sn}".format(
        pn=promedios['Precision No humor'], rn=promedios['Recall No humor'], fn=promedios['F1-score No humor'],
        sn=tn + fp))
    print("     Humor        {pp:0.4f}      {rp:0.4f}      {fp:0.4f}      {sp}".format(
        pp=promedios['Precision Humor'], rp=promedios['Recall Humor'], fp=promedios['F1-score Humor'], sp=tp + fn))
    print('')
    print("avg / total       {ap:0.4f}      {ar:0.4f}      {af:0.4f}      {su}".format(
        ap=(promedios['Precision Humor'] + promedios['Precision No humor']) / 2,
        ar=(promedios['Recall Humor'] + promedios['Recall No humor']) / 2,
        af=(promedios['F1-score Humor'] + promedios['F1-score No humor']) / 2,
        su=tp + fp + tn + fn
    ))
    print('')
    imprimir_matriz_de_confucion(tp, fp, tn, fn)
    return verdaderos_positivos, falsos_negativos, falsos_positivos, verdaderos_negativos


def imprimir_matriz_de_confucion(tp, fp, tn, fn):
    print("Matriz de confusión:")
    print('')
    print("\t\t\t(clasificados como)")
    print("\t\t\tHumor\tNo humor")
    if type(tp) == float:
        print("(son)\tHumor\t\t{vp:0.4f}\t{fn:0.4f}".format(vp=tp, fn=fn))
        print("(son)\tNo humor\t{fp:0.4f}\t{vn:0.4f}".format(fp=fp, vn=tn))
    else:
        print("(son)\tHumor\t\t{vp: <5d}\t{fn: <5d}".format(vp=tp, fn=fn))
        print("(son)\tNo humor\t{fp: <5d}\t{vn: <5d}".format(fp=fp, vn=tn))
    print('')