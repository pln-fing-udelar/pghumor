#!/usr/bin/env python2
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import random
import sys

from flask import Flask, request
from flask_cors import cross_origin
from sklearn import linear_model, naive_bayes, neighbors, preprocessing, svm, tree
from sklearn.feature_selection import RFECV
from sklearn.grid_search import GridSearchCV


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.define import parameters_svm, parameters_dt, \
    parameters_gnb, parameters_mnb, parameters_knn
from clasificador.features.features import Features
from clasificador.herramientas.persistencia import cargar_tweets, guardar_features
from clasificador.herramientas.utilclasificacion import cross_validation_y_reportar, \
    get_clases, get_features, matriz_de_confusion_y_reportar, train_test_split_pro
from clasificador.herramientas.utilanalisis import chi2_feature_selection, \
    f_score_feature_selection, imprimir_importancias, tree_based_feature_selection
from clasificador.herramientas.utils import filtrar_segun_votacion
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
                        help='muestra las features disponibles y termina el programa')
    parser.add_argument('-j', '--feature-aleatoria', action='store_true', default=False,
                        help='agrega una feature con un valor binario aleatorio')
    parser.add_argument('-k', '--feature-clase', action='store_true', default=False,
                        help='agrega una feature cuyo valor es igual a la clase objetivo')
    parser.add_argument('-g', '--grid-search', action='store_true', default=False,
                        help="realiza el algoritmo grid search para el tuning de hyperparametros")
    parser.add_argument('-i', '--importancias-features', action='store_true', default=False,
                        help="reporta la importancia de cada feature")
    parser.add_argument('-l', '--limite', type=int, help="establece una cantidad límite de tweets a procesar")
    parser.add_argument('-p', '--parametros-clasificador', action='store_true', default=False,
                        help="lista los parametros posibles para un clasificador")
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
    args = parser.parse_args()

    if args.explicar_features:
        features_obj = Features(args.threads)
        for feature in sorted(list(features_obj.features.values()), key=lambda x: x.nombre):
            print(feature.nombre + ":")
            print(feature.descripcion)
    else:
        corpus = cargar_tweets(args.limite)

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

        if args.feature_aleatoria or args.feature_clase:
            for tweet in corpus:
                if args.feature_aleatoria:
                    tweet.features['ALEATORIA'] = random.uniform(0, 1)
                if args.feature_clase:
                    tweet.features['CLASE'] = tweet.es_humor

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
            print("Acierto: " + str(grid_search.best_score_))
            grid_search.best_estimator_ = grid_search.best_estimator_.fit(features, clases)
            clasificador_usado = grid_search.best_estimator_
            print("")

        if args.parametros_clasificador:
            print("")
            print("Parametros del clasificador:")
            for key, value in clasificador_usado.get_params().items():
                print("\t" + str(key) + ": " + str(value))
            print("")

        if args.cross_validation and not args.evaluar:
            cross_validation_y_reportar(clasificador_usado, features, clases, 5)

        print("Entrenando clasificador...")
        clasificador_usado.fit(features_entrenamiento, clases_entrenamiento)
        print("Evaluando clasificador...")
        clases_predecidas = clasificador_usado.predict(features_evaluacion)
        print('')

        verdaderos_positivos, falsos_negativos, falsos_positivos, verdaderos_negativos = matriz_de_confusion_y_reportar(
            evaluacion, clases_evaluacion, clases_predecidas)

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
