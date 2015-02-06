#!/usr/bin/env python2
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import random
import sys
import itertools

from flask import Flask, request
from flask_cors import cross_origin
from progress.bar import Bar
from sklearn import linear_model, naive_bayes, neighbors, preprocessing, svm, tree
from sklearn.feature_selection import RFECV
from sklearn.grid_search import GridSearchCV

from clasificador.herramientas.freeling import Freeling


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.define import parameters_svm, parameters_dt, \
    parameters_gnb, parameters_mnb, parameters_knn, SUFIJO_PROGRESS_BAR
from clasificador.features.features import Features
from clasificador.herramientas.persistencia import cargar_tweets, guardar_features
from clasificador.herramientas.utilclasificacion import cross_validation_y_reportar, \
    get_clases, get_features, matriz_de_confusion_y_reportar, train_test_split_pro
from clasificador.herramientas.utilanalisis import chi2_feature_selection, \
    f_score_feature_selection, imprimir_importancias, tree_based_feature_selection
from clasificador.herramientas.utils import entropia, filtrar_segun_votacion, distancia_edicion
from clasificador.realidad.tweet import Tweet

# Ver esto: http://ceur-ws.org/Vol-1086/paper12.pdf
# Ver esto: https://stackoverflow.com/questions/8764066/preprocessing-400-million-tweets-in-python-faster
# Ver esto: https://www.google.com.uy/search?q=preprocess+tweet+like+normal+text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clasifica humor de los tweets almacenados en la base de datos.')
    parser.add_argument('-a', '--calcular-features-faltantes', action='store_true', default=False,
                        help="calcula el valor de todas las features para los tweets a los que les falta calcularla")
    parser.add_argument('-c', '--clasificador', type=str, default="SVM",
                        choices=["DT", "GNB", "kNN", "LinearSVM", "MNB", "SGD", "SVM"],
                        help="establece qué tipo de clasificador será usado, que por defecto es SVM")
    parser.add_argument('-x', '--cross-validation', action='store_true', default=False,
                        help="para hacer cross-validation")
    parser.add_argument('-e', '--evaluar', action='store_true', default=False,
                        help="para evaluar con el corpus de evaluación")
    parser.add_argument('-b', '--explicar-features', action='store_true', default=False,
                        help="muestra las features disponibles y termina el programa")
    parser.add_argument('-j', '--feature-aleatoria', action='store_true', default=False,
                        help="agrega una feature con un valor binario aleatorio")
    parser.add_argument('-k', '--feature-clase', action='store_true', default=False,
                        help="agrega una feature cuyo valor es igual a la clase objetivo")
    parser.add_argument('-g', '--grid-search', action='store_true', default=False,
                        help="realiza el algoritmo grid search para el tuning de hyperparametros")
    parser.add_argument('-i', '--importancias-features', action='store_true', default=False,
                        help="reporta la importancia de cada feature")
    parser.add_argument('-z', '--incluir-chistes-sexuales', action='store_true', default=False,
                        help="Incluye en el entrenamiento y en la evaluación los chistes con contenido sexual")
    parser.add_argument('-l', '--limite', type=int, help="establece una cantidad límite de tweets a procesar")
    parser.add_argument('-m', '--mismas-features-distinto-humor', action='store_true', default=False,
                        help="Imprime los tweets que tienen los mismos valores de features"
                             + " pero distinto valor de humor")
    parser.add_argument('-q', '--medidas-ponderadas', action='store_true', default=False,
                        help="Imprime las medidas precision, recall, f1-score ponderadas según el promedio de humor"
                             + " pero distinto valor de humor")
    parser.add_argument('-p', '--parametros-clasificador', action='store_true', default=False,
                        help="lista los parametros posibles para un clasificador")
    parser.add_argument('-n', '--ponderar-segun-votos', action='store_true', default=False,
                        help="en la clasificación pondera los tweets según la concordancia en la votación"
                             + " Funciona sólo para SVM")
    parser.add_argument('-s', '--recalcular-features', action='store_true', default=False,
                        help="recalcula el valor de todas las features")
    parser.add_argument('-f', '--recalcular-feature', type=str, metavar="NOMBRE_FEATURE",
                        help="recalcula el valor de una feature")
    parser.add_argument('-d', '--rfe', action='store_true', default=False,
                        help="habilita el uso de Recursive Feature Elimination antes de clasificar")
    parser.add_argument('-r', '--servidor', action='store_true', default=False,
                        help="levanta el servidor para responder a clasificaciones")
    parser.add_argument('-t', '--threads', type=int,
                        help="establece la cantidad de threads a usar al recalcular las features", default=1)
    parser.add_argument('-o', '--tweets-parecidos-distinto-humor', action='store_true', default=False,
                        help="Imprime los tweets que son parecidos pero distinto valor de humor")
    args = parser.parse_args()

    if args.explicar_features:
        features_obj = Features(args.threads)
        for feature in sorted(list(features_obj.features.values()), key=lambda x: x.nombre):
            print(feature.nombre + ":")
            print(feature.descripcion)
    else:
        corpus = cargar_tweets(args.limite, args.incluir_chistes_sexuales)

        for tweet in corpus:
            tweet.preprocesar()

        if args.recalcular_features:
            features_obj = Features(args.threads)
            features_obj.calcular_features(corpus)
            guardar_features(corpus)
        elif args.recalcular_feature:
            features_obj = Features(args.threads)
            features_obj.calcular_feature(corpus, args.recalcular_feature.decode('utf-8'))
            guardar_features(corpus, nombre_feature=args.recalcular_feature.decode('utf-8'))
        elif args.calcular_features_faltantes:
            features_obj = Features(args.threads)
            features_obj.calcular_features_faltantes(corpus)
            guardar_features(corpus)

        corpus = filtrar_segun_votacion(corpus)

        if args.evaluar:
            entrenamiento = [tweet for tweet in corpus if not tweet.evaluacion]
            evaluacion = [tweet for tweet in corpus if tweet.evaluacion]
        else:
            corpus = [tweet for tweet in corpus if not tweet.evaluacion]
            entrenamiento, evaluacion = train_test_split_pro(corpus, test_size=0.2)

        if args.tweets_parecidos_distinto_humor:
            print("Buscando tweets muy parecidos pero con distinto valor de humor...")

            bar = Bar("Tokenizando", max=len(corpus), suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)
            for tweet in corpus:
                tweet.oraciones = Freeling.procesar_texto(tweet.texto_original)
                tweet.tokens = list(itertools.chain(*tweet.oraciones))
                bar.next()

            bar.finish()

            bar = Bar("Buscando en tweets", max=len(corpus) * (len(corpus) - 1) / 2, suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)

            parecidos_con_distinto_humor = set()

            for tweet1 in corpus:
                for tweet2 in corpus:
                    if tweet1.id < tweet2.id:
                        bar.next()
                        if tweet1.es_humor != tweet2.es_humor \
                                and distancia_edicion(tweet1.tokens, tweet2.tokens) \
                                        <= max(len(tweet1.tokens), len(tweet2.tokens)) / 5:
                            parecidos_con_distinto_humor.add(tweet1)
                            parecidos_con_distinto_humor.add(tweet2)
                            print(tweet1.id)
                            print(tweet1.texto_original)
                            print("------------")
                            print(tweet2.id)
                            print(tweet2.texto_original)
                            print("------------")
                            print('')

            bar.finish()

            corpus = [tweet for tweet in corpus if tweet not in parecidos_con_distinto_humor]

        if args.mismas_features_distinto_humor:
            print("Buscando tweets con mismos valores de features pero distinto de humor...")
            bar = Bar("Buscando en tweets", max=len(corpus) * len(corpus), suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)
            for tweet1 in corpus:
                for tweet2 in corpus:
                    bar.next()
                    if tweet1.id < tweet2.id and tweet1.features == tweet2.features \
                            and tweet1.es_humor != tweet2.es_humor:
                        if tweet1.texto_original == tweet2.texto_original:
                            print("-----MISMO TEXTO ORIGINAL------")
                        if tweet1.texto == tweet2.texto:
                            print("----------MISMO TEXTO----------")
                        if tweet1.id == tweet2.id:
                            print("-----------MISMO ID------------")
                        if tweet1.cuenta == tweet2.cuenta:
                            print("----------MISMA CUENTA---------")
                        print(tweet1.id)
                        print(tweet1.texto)
                        print("------------")
                        print(tweet2.id)
                        print(tweet2.texto)
                        print("------------")
                        print('')

            bar.finish()

        if args.feature_aleatoria or args.feature_clase:
            for tweet in corpus:
                if args.feature_aleatoria:
                    tweet.features["ALEATORIA"] = random.uniform(0, 1)
                if args.feature_clase:
                    tweet.features["CLASE"] = tweet.es_humor

        # Features que remueve RFE:
        # for tweet in corpus:
        # del tweet.features["Palabras no españolas"]
        # del tweet.features["Negacion"]

        clases = get_clases(corpus)
        clases_entrenamiento = get_clases(entrenamiento)
        clases_evaluacion = get_clases(evaluacion)

        features = get_features(corpus)
        features_entrenamiento = get_features(entrenamiento)
        features_evaluacion = get_features(evaluacion)

        # Se tiene que hacer antes del scaler (las features no puden tomar valores negativos)
        if args.importancias_features:
            nombres_features_ordenadas = corpus[0].nombres_features_ordenadas()
            tree_based_feature_selection(features, clases, nombres_features_ordenadas)
            chi2_feature_selection(features, clases, nombres_features_ordenadas)
            f_score_feature_selection(features, clases, nombres_features_ordenadas)

        if args.clasificador != "MNB":
            scaler = preprocessing.StandardScaler().fit(features_entrenamiento)
            features = scaler.transform(features)
            features_entrenamiento = scaler.transform(features_entrenamiento)
            features_evaluacion = scaler.transform(features_evaluacion)

        if args.rfe:
            rfecv = RFECV(estimator=svm.SVC(kernel=str('linear')), cv=5, scoring='accuracy', verbose=3)
            rfecv.fit(features_entrenamiento, clases_entrenamiento)

            print("Número óptimo de featues: %d" % rfecv.n_features_)

            nombres_features_ordenadas = corpus[0].nombres_features_ordenadas()
            imprimir_importancias(rfecv.ranking_, "RFECV", nombres_features_ordenadas)

            # Esto saca "Palabras no españolas" y "Negación".

        parameters_grid_search = {}
        if args.clasificador == "DT":
            clasificador_usado = tree.DecisionTreeClassifier()
            parameters_grid_search = parameters_dt
        elif args.clasificador == "GNB":
            clasificador_usado = naive_bayes.GaussianNB()
            parameters_grid_search = parameters_gnb
        elif args.clasificador == "kNN":
            clasificador_usado = neighbors.KNeighborsClassifier()
            parameters_grid_search = parameters_knn
        elif args.clasificador == "LinearSVM":
            clasificador_usado = svm.LinearSVC()
        elif args.clasificador == "MNB":
            clasificador_usado = naive_bayes.MultinomialNB()
            parameters_grid_search = parameters_mnb
        elif args.clasificador == "SGD":
            clasificador_usado = linear_model.SGDClassifier(shuffle=True)
        else:  # "SVM"
            clasificador_usado = svm.SVC()
            parameters_grid_search = parameters_svm

        if args.grid_search:
            grid_search = GridSearchCV(clasificador_usado, parameters_grid_search, cv=5, verbose=2, n_jobs=8)

            grid_search.fit(features, clases)
            print("Mejores parámetros encontrados para " + args.clasificador + ":")
            for key, value in clasificador_usado.get_params().items():
                print("\t" + unicode(key) + ": " + unicode(value))
            print('')
            print("Acierto: " + unicode(grid_search.best_score_))
            grid_search.best_estimator_ = grid_search.best_estimator_.fit(features, clases)
            clasificador_usado = grid_search.best_estimator_
            print('')

        if args.parametros_clasificador:
            print('')
            print("Parametros del clasificador:")
            for key, value in clasificador_usado.get_params().items():
                print("\t" + unicode(key) + ": " + unicode(value))
            print('')

        if args.cross_validation and not args.evaluar:
            cross_validation_y_reportar(clasificador_usado, features, clases, 5)

        print("Entrenando clasificador...")
        if args.ponderar_segun_votos:
            sample_weights = [5 * (1 - entropia(tweet.votos_humor / float(tweet.votos))) if tweet.votos > 0 else 1
                              for tweet in entrenamiento]
            clasificador_usado.fit(features_entrenamiento, clases_entrenamiento, sample_weight=sample_weights)
        else:
            clasificador_usado.fit(features_entrenamiento, clases_entrenamiento)

        print("Evaluando clasificador con conjunto de entrenamiento...")
        clases_predecidas_entrenamiento = clasificador_usado.predict(features_entrenamiento)
        matriz_de_confusion_y_reportar(entrenamiento, clases_entrenamiento, clases_predecidas_entrenamiento,
                                       args.medidas_ponderadas)
        print('')

        print("Evaluando clasificador...")
        clases_predecidas = clasificador_usado.predict(features_evaluacion)
        print('')

        verdaderos_positivos, falsos_negativos, falsos_positivos, verdaderos_negativos = matriz_de_confusion_y_reportar(
            evaluacion, clases_evaluacion, clases_predecidas, args.medidas_ponderadas)

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
                _features_obj = Features(args.threads)
                _features_obj.calcular_features([_tweet])
                _features = [list(_tweet.features.values())]
                return str(int(clasificador_usado.predict(_features)[0]))

            app.run(debug=True, host='0.0.0.0')
