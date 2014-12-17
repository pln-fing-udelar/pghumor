#!/usr/bin/env python2
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import argparse
from flask import Flask, request
from flask_cors import cross_origin
import numpy
import os
import random
from sklearn import cross_validation
from sklearn import naive_bayes, svm
from sklearn import metrics
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.realidad.tweet import Tweet
from clasificador.features.features import Features
from clasificador.herramientas.persistencia import cargar_tweets, guardar_features


def train_test_split_pro(_corpus, **options):
    """Es como el de sklearn, pero como no deja saber qué tweets están en qué conjunto,
    hicimos este.
    # features_entrenamiento, features_evaluacion, clases_entrenamiento, clases_evaluacion
    # = train_test_split(features, clases, test_size=fraccion_evaluacion)

    """
    fraccion_evaluacion = options.pop('test_size', 0.25)

    elegir_fraccion = random.sample(range(len(_corpus)), int(len(_corpus) * fraccion_evaluacion))
    _entrenamiento = [_corpus[j] for j in range(len(_corpus)) if j not in elegir_fraccion]
    _evaluacion = [_corpus[j] for j in elegir_fraccion]

    return _entrenamiento, _evaluacion


def features_clases_split(tweets):
    assert len(tweets) > 0, "Deben haber tweets para obtener las features y las clases"
    largo_esperado_features = len(list(tweets[0].features.values()))
    _features = []
    for _tweet in tweets:
        features_tweet = list(_tweet.features.values())
        assert len(features_tweet) == largo_esperado_features, "Los tweets tienen distinta cantidad de features"
        _features.append(features_tweet)
    _clases = numpy.array([_tweet.es_humor for _tweet in tweets], dtype=float)
    return _features, _clases


def filtrar_segun_votacion(_corpus):
    res = []
    for _tweet in _corpus:
        if _tweet.es_humor:
            if _tweet.votos > 0:
                porcentaje_humor = _tweet.votos_humor / float(_tweet.votos)
                if porcentaje_humor >= 0.60:
                    res.append(_tweet)
                elif porcentaje_humor <= 0.30:
                    _tweet.es_humor = False
                    res.append(_tweet)
        else:
            res.append(_tweet)
    return res

# Ver esto: http://ceur-ws.org/Vol-1086/paper12.pdf

# Ver esto: https://stackoverflow.com/questions/8764066/preprocessing-400-million-tweets-in-python-faster

# Ver esto: https://www.google.com.uy/search?q=preprocess+tweet+like+normal+text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clasifica humor de los tweets almacenados en MySQL.')
    parser.add_argument('-a', '--calcular-features-faltantes', action='store_true', default=False,
                        help="calcula el valor de todas las features para los tweets a los que les falta calcularla")
    parser.add_argument('-c', '--clasificador', type=str, default="SVM", choices=["GNB", "MNB", "SVM"],
                        help="establece qué tipo de clasificador será usado, que por defecto es SVM")
    parser.add_argument('-x', '--cross-validation', action='store_true', default=False,
                        help="para hacer cross-validation")
    parser.add_argument('-e', '--evaluar', action='store_true', default=False,
                        help="para evaluar con el corpus de evaluación")
    parser.add_argument('-b', '--explicar-features', action='store_true', default=False,
                        help='muestra las features disponibles y termina el programa')
    parser.add_argument('-l', '--limite', type=int, help="establece una cantidad límite de tweets a procesar")
    parser.add_argument('-p', '--prueba', action='store_true', default=False,
                        help="establece el modo prueba")
    parser.add_argument('-s', '--recalcular-features', action='store_true', default=False,
                        help="recalcula el valor de todas las features")
    parser.add_argument('-f', '--recalcular-feature', type=str, metavar="NOMBRE_FEATURE",
                        help="recalcula el valor de una feature")
    parser.add_argument('-r', '--servidor', action='store_true', default=False,
                        help="levanta el servidor para responder a clasificaciones")

    args = parser.parse_args()

    if args.explicar_features:
        features_obj = Features()
        for feature in sorted(list(features_obj.features.values()), key=lambda x: x.nombre):
            print(feature.nombre + ":")
            print(feature.descripcion)
    else:
        corpus = cargar_tweets(args.prueba)

        if args.limite:
            elegir_algunos = random.sample(range(len(corpus)), args.limite)
            corpus = [corpus[i] for i in range(len(corpus)) if i in elegir_algunos]

        for tweet in corpus:
            tweet.preprocesar()

        if args.recalcular_features:
            features_obj = Features()
            features_obj.calcular_features(corpus)
            guardar_features(corpus)
        elif args.recalcular_feature:
            features_obj = Features()
            features_obj.calcular_feature(corpus, args.recalcular_feature)
            guardar_features(corpus, nombre_feature=args.recalcular_feature)
        elif args.calcular_features_faltantes:
            features_obj = Features()
            features_obj.calcular_features_faltantes(corpus)
            guardar_features(corpus)

        corpus = filtrar_segun_votacion(corpus)

        # print("Realizando método de aprendizaje automático")
        if args.evaluar:
            entrenamiento = [tweet for tweet in corpus if not tweet.evaluacion]
            evaluacion = [tweet for tweet in corpus if tweet.evaluacion]
        else:
            corpus = [tweet for tweet in corpus if not tweet.evaluacion]
            # humor = [tweet for tweet in corpus if tweet.es_humor]
            # nohumor = [tweet for tweet in corpus if not tweet.es_humor]
            # if len(humor) > len(nohumor):
            # corpus = nohumor + humor[:len(nohumor)]
            # else:
            # corpus = nohumor[:len(humor)] + humor

            entrenamiento, evaluacion = train_test_split_pro(corpus, test_size=0.2)

        features_entrenamiento, clases_entrenamiento = features_clases_split(entrenamiento)
        features_evaluacion, clases_evaluacion = features_clases_split(evaluacion)

        if args.clasificador == "MNB":
            clasificador_usado = naive_bayes.MultinomialNB()
        elif args.clasificador == "GNB":
            clasificador_usado = naive_bayes.GaussianNB()
        else:  # "SVM"
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
        print('\t\t\tP\tN')
        print('(son)\tP\t' + str(len(verdaderos_positivos)) + '\t' + str(len(falsos_negativos)))
        print('(son)\tN\t' + str(len(falsos_positivos)) + '\t' + str(len(verdaderos_negativos)))
        print('')

        if args.servidor:
            app = Flask(__name__)

            @app.route("/")
            def inicio():
                return app.send_static_file('evaluacion.html')

            @app.route("/evaluar", methods=['POST'])
            @cross_origin()
            def evaluar():
                _tweet = Tweet()
                _tweet.texto = request.form['texto']
                _tweet.preprocesar()
                _features_obj = Features()
                _features_obj.calcular_features([_tweet])
                _features = [list(_tweet.features.values())]
                return str(int(clasificador_usado.predict(_features)[0]))

            app.run(debug=True, host='0.0.0.0')
