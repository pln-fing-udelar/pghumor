#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
import argparse

import numpy
from sklearn import cross_validation
from sklearn import naive_bayes, svm
from sklearn import metrics

import clasificador.herramientas.persistencia
from clasificador.features.features import Features


def train_test_split_pro(corpus, **options):
    # El de sklearn no deja saber qué tweets están en qué conjunto.
    # features_entrenamiento, features_evaluacion, clases_entrenamiento, clases_evaluacion \
    # = train_test_split(features, clases, test_size=fraccion_evaluacion)

    fraccion_evaluacion = options.pop('test_size', 0.25)

    elegir_fraccion = random.sample(range(len(corpus)), int(len(corpus) * fraccion_evaluacion))
    entrenamiento = [corpus[i] for i in range(len(corpus)) if i not in elegir_fraccion]
    evaluacion = [corpus[i] for i in elegir_fraccion]

    return entrenamiento, evaluacion


def features_clases_split(tweets):
    features = numpy.array([numpy.array(tweet.features.values()) for tweet in tweets])
    clases = numpy.array([tweet.es_humor for tweet in tweets], dtype=float)
    return features, clases

# Ver esto: http://ceur-ws.org/Vol-1086/paper12.pdf

# Ver esto: https://stackoverflow.com/questions/8764066/preprocessing-400-million-tweets-in-python-faster

# Ver esto: https://www.google.com.uy/search?q=process+tweet+like+normal+text&oq=process+tweet+like+normal+text&aqs=chrome..69i57j69i60l4j69i61.4367j0j7&sourceid=chrome&es_sm=93&ie=UTF-8#q=preprocess+tweet+like+normal+text

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--cross-validation', action='store_true', default=False)
    parser.add_argument('--evaluar', action='store_true', default=False)
    parser.add_argument('--explicar-features', action='store_true', default=False)
    parser.add_argument('--limit', type=int)
    parser.add_argument('--recalcular-features', action='store_true', default=False)
    parser.add_argument('--recalcular-feature', type=str)

    args = parser.parse_args()

    if args.explicar_features:
        features_obj = Features()
        for feature in sorted(list(features_obj.features.values()), key=lambda x: x.nombre):
            print(feature.nombre + ":")
            print(feature.descripcion)
    else:
        corpus = clasificador.herramientas.persistencia.cargar_tweets(cargar_evaluacion=args.evaluar)

        if args.limit is not None:
            elegir_algunos = random.sample(range(len(corpus)), args.limit)
            corpus = [corpus[i] for i in range(len(corpus)) if i in elegir_algunos]

        for tweet in corpus:
            tweet.preprocesar()

        if args.recalcular_features:
            features_obj = Features()
            features_obj.calcular_features(corpus)
            clasificador.herramientas.persistencia.guardar_features(corpus)
        elif args.recalcular_feature is not None:
            features_obj = Features()
            features_obj.calcular_feature(corpus, args.recalcular_feature)
            clasificador.herramientas.persistencia.guardar_features(corpus, nombre_feature=args.recalcular_feature)

        #print("Realizando método de aprendizaje automático")
        if args.evaluar:
            entrenamiento = [tweet for tweet in corpus if not tweet.evaluacion]
            evaluacion = [tweet for tweet in corpus if tweet.evaluacion]
        else:
            humor = [tweet for tweet in corpus if tweet.es_humor]
            nohumor = [tweet for tweet in corpus if not tweet.es_humor]
            # if len(humor) > len(nohumor):
            # corpus = nohumor + humor[:len(nohumor)]
            #else:
            #	corpus = nohumor[:len(humor)] + humor

            entrenamiento, evaluacion = train_test_split_pro(corpus, test_size=0.2)

        features_entrenamiento, clases_entrenamiento = features_clases_split(entrenamiento)
        features_evaluacion, clases_evaluacion = features_clases_split(evaluacion)

        # clasificador_usado = naive_bayes.GaussianNB()
        # clasificador_usado = naive_bayes.MultinomialNB()
        clasificador_usado = svm.SVC()

        if args.cross_validation and not args.evaluar:
            features, clases = features_clases_split(corpus)

            puntajes = cross_validation.cross_val_score(clasificador_usado, features, clases, cv=5, verbose=True)
            print('Cross-validation:')
            print('')
            print('Puntajes: ' + str(puntajes))
            print("Acierto: %0.4f (+/- %0.4f)" % (puntajes.mean(), puntajes.std() * 2))
            print('')
            print('')

        clasificador_usado.fit(features_entrenamiento, clases_entrenamiento)

        clases_predecidas = clasificador_usado.predict(features_evaluacion)

        verdaderos_positivos = [evaluacion[i] for i in range(len(evaluacion)) if
                                clases_predecidas[i] and clases_evaluacion[i]]
        falsos_positivos = [evaluacion[i] for i in range(len(evaluacion)) if
                            clases_predecidas[i] and not clases_evaluacion[i]]
        falsos_negativos = [evaluacion[i] for i in range(len(evaluacion)) if
                            not clases_predecidas[i] and clases_evaluacion[i]]
        verdaderos_negativos = [evaluacion[i] for i in range(len(evaluacion)) if
                                not clases_predecidas[i] and not clases_evaluacion[i]]

        # Reporte de estadísticas

        print(metrics.classification_report(clases_evaluacion, clases_predecidas, target_names=['N', 'P']))
        print('')

        print('Acierto: ' + str(metrics.accuracy_score(clases_evaluacion, clases_predecidas)))
        print('')

        matriz_de_confusion = metrics.confusion_matrix(clases_evaluacion, clases_predecidas, labels=[True, False])
        # Con 'labels' pido el orden para la matriz

        assert len(verdaderos_positivos) == matriz_de_confusion[0][0]
        assert len(falsos_negativos) == matriz_de_confusion[0][1]
        assert len(falsos_positivos) == matriz_de_confusion[1][0]
        assert len(verdaderos_negativos) == matriz_de_confusion[1][1]

        print('Matriz de confusión:')
        print('')
        print('\t\t(clasificados como)')
        print('\t\tP\tN')
        print('(son)\tP\t' + str(len(verdaderos_positivos)) + '\t' + str(len(falsos_negativos)))
        print('(son)\tN\t' + str(len(falsos_positivos)) + '\t' + str(len(verdaderos_negativos)))
        print('')
