#!/usr/bin/env python2
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import argparse
import os
import sys

from flask import Flask, request
from flask_cors import cross_origin
from sklearn import linear_model, naive_bayes, preprocessing, svm, tree
from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.pipeline import Pipeline


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.realidad.tweet import Tweet
from clasificador.features.features import Features
from clasificador.herramientas.persistencia import cargar_tweets, guardar_features
from clasificador.herramientas.utilclasificacion import cross_validation_y_reportar, \
    get_clases, get_features, matriz_de_confusion_y_reportar, train_test_split_pro
from clasificador.herramientas.utils import filtrar_segun_votacion, get_stop_words


# Ver esto: http://ceur-ws.org/Vol-1086/paper12.pdf
# Ver esto: https://stackoverflow.com/questions/8764066/preprocessing-400-million-tweets-in-python-faster
# Ver esto: https://www.google.com.uy/search?q=preprocess+tweet+like+normal+text

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Clasifica humor de los tweets almacenados en MySQL.')
    parser.add_argument('-a', '--calcular-features-faltantes', action='store_true', default=False,
                        help="calcula el valor de todas las features para los tweets a los que les falta calcularla")
    parser.add_argument('-c', '--clasificador', type=str, default="SVM",
                        choices=["DT", "GNB", "LinearSVM", "MNB", "SGD", "SVM"],
                        help="establece qué tipo de clasificador será usado, que por defecto es SVM")
    parser.add_argument('-x', '--cross-validation', action='store_true', default=False,
                        help="para hacer cross-validation")
    parser.add_argument('-e', '--evaluar', action='store_true', default=False,
                        help="para evaluar con el corpus de evaluación")
    parser.add_argument('-b', '--explicar-features', action='store_true', default=False,
                        help='muestra las features disponibles y termina el programa')
    parser.add_argument('-i', '--importancias-features', action='store_true', default=False,
                        help="reporta la importancia de cada feature")
    parser.add_argument('-l', '--limite', type=int, help="establece una cantidad límite de tweets a procesar")
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
        corpus = cargar_tweets(args.limite)

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

        if args.evaluar:
            entrenamiento = [tweet for tweet in corpus if not tweet.evaluacion]
            evaluacion = [tweet for tweet in corpus if tweet.evaluacion]
        else:
            corpus = [tweet for tweet in corpus if not tweet.evaluacion]
            entrenamiento, evaluacion = train_test_split_pro(corpus, test_size=0.2)

        clases = get_clases(corpus)
        clases_entrenamiento = get_clases(entrenamiento)
        clases_evaluacion = get_clases(evaluacion)

        # TODO: poner en una clase
        features_texto_entrenamiento = [tweet.texto for tweet in entrenamiento]
        bow = Pipeline([
            ('vect', CountVectorizer(
                stop_words=get_stop_words(),
                token_pattern=r'\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b',
            )),
            ('clf', naive_bayes.MultinomialNB(alpha=0.01)),
        ])
        bow = bow.fit(features_texto_entrenamiento, clases_entrenamiento)
        for tweet in corpus:
            tweet.predict_proba = bow.predict_proba([tweet.texto])[0][0]

        features = get_features(corpus)
        features_entrenamiento = get_features(entrenamiento)
        features_evaluacion = get_features(evaluacion)

        # TODO: poner en pipeline
        scaler = preprocessing.StandardScaler().fit(features_entrenamiento)
        features = scaler.transform(features)
        features_entrenamiento = scaler.transform(features_entrenamiento)
        features_evaluacion = scaler.transform(features_evaluacion)

        if args.clasificador == "DT":
            clasificador_usado = tree.DecisionTreeClassifier()
        elif args.clasificador == "GNB":
            clasificador_usado = naive_bayes.GaussianNB()
        elif args.clasificador == "LinearSVM":
            clasificador_usado = svm.LinearSVC()
        elif args.clasificador == "MNB":
            clasificador_usado = naive_bayes.MultinomialNB()
        elif args.clasificador == "SGD":
            clasificador_usado = linear_model.SGDClassifier(shuffle=True)
        else:  # "SVM"
            clasificador_usado = svm.SVC()

        if args.importancias_features:
            clf = ExtraTreesClassifier()
            clf.fit(features, clases)

            features_ordenadas = corpus[0].features_ordenadas()

            importancias = {}
            for i in range(len(features_ordenadas)):
                importancias[features_ordenadas[i]] = clf.feature_importances_[i]

            importancias["BOW"] = clf.feature_importances_[len(features_ordenadas)]

            print("Ranking de features:")

            for nombre_feature in sorted(importancias, key=importancias.get, reverse=True):
                print(nombre_feature, importancias[nombre_feature])

        if args.cross_validation and not args.evaluar:
            cross_validation_y_reportar(clasificador_usado, features, clases, 5)

        print('')
        print("Entrenando clasificador...")
        print('')

        clasificador_usado.fit(features_entrenamiento, clases_entrenamiento)

        print('')
        print("Evaluando clasificador...")
        print('')

        clases_predecidas = clasificador_usado.predict(features_evaluacion)

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
                _features_obj = Features()
                _features_obj.calcular_features([_tweet])
                _features = [list(_tweet.features.values())]
                return str(int(clasificador_usado.predict(_features)[0]))

            app.run(debug=True, host='0.0.0.0')
