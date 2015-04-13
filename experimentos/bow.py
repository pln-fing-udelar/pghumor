#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
import argparse
import os
import sys

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline, FeatureUnion


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.persistencia import cargar_tweets
from clasificador.herramientas.utilclasificacion import get_clases, \
    matriz_de_confusion_y_reportar, train_test_split_pro
from clasificador.herramientas.utils import filtrar_segun_votacion, get_stop_words

from experimentos.tweettotext import TweetToText
from experimentos.tweetstofeatures import TweetsToFeatures

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Clasifica humor de los tweets almacenados en la base de datos, utilizando BOW.')
    parser.add_argument('-e', '--evaluar', action='store_true', default=False,
                        help="para evaluar con el corpus de evaluación")
    parser.add_argument('-C', '--reportar-informacion-corpus', action='store_true', default=False,
                        help="reporta cómo está conformado el corpus")
    args = parser.parse_args()

    corpus = cargar_tweets(cargar_features=True)
    print('')
    print('')

    print("Filtrando y corrigiendo según la votación...")
    filtrar_segun_votacion(corpus)

    print("Separando en entrenamiento y evaluación...")

    if args.evaluar:
        entrenamiento = [tweet for tweet in corpus if not tweet.evaluacion]
        evaluacion = [tweet for tweet in corpus if tweet.evaluacion]
    else:
        corpus = [tweet for tweet in corpus if not tweet.evaluacion]
        entrenamiento, evaluacion = train_test_split_pro(corpus, test_size=0.2)

    if args.reportar_informacion_corpus:
        print('')
        print("Conformación del corpus")
        print("                 Entrenamiento Evaluacion Total")
        print("    Humor        {he}          {ht}       {htot}".format(
            he=len([tweet for tweet in entrenamiento if tweet.es_humor]),
            ht=len([tweet for tweet in evaluacion if tweet.es_humor]),
            htot=len([tweet for tweet in corpus if tweet.es_humor])
        ))
        print("    No humor     {nhe}         {nht}       {nhtot}".format(
            nhe=len([tweet for tweet in entrenamiento if not tweet.es_humor]),
            nht=len([tweet for tweet in evaluacion if not tweet.es_humor]),
            nhtot=len([tweet for tweet in corpus if not tweet.es_humor])
        ))
        print("    Total        {te}         {tt}       {t}".format(
            te=len(entrenamiento),
            tt=len(evaluacion),
            t=len(corpus)
        ))
        print('')

    print("Separando tweets en features y clases...")
    X = [tweet for tweet in corpus]
    y = get_clases(corpus)

    X_train = [tweet for tweet in entrenamiento]
    X_test = [tweet for tweet in evaluacion]

    y_train = get_clases(entrenamiento)
    y_test = get_clases(evaluacion)

    feature_union = FeatureUnion([
        ('vectorizer_bow', Pipeline([
            ('tweet_to_text', TweetToText()),
            ('vectorizer', CountVectorizer(
                strip_accents='ascii',
                stop_words=get_stop_words(),
                token_pattern=r'\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b',
            ))
        ])),
        ('features_tweets', TweetsToFeatures()),
    ])

    clasificador = Pipeline([
        ('features', feature_union),
        # ('scaler', preprocessing.StandardScaler()),
        # ('features_tweets', TweetsToFeatures()),
        ('clf', MultinomialNB(alpha=0.01)),
    ])

    print('')
    print('')

    # cross_validation_y_reportar(clasificador, X, y, 5)

    print("Entrenando clasificador...")
    clasificador.fit(X_train, y_train)

    print("Evaluando clasificador...")
    print('')
    y_pred = clasificador.predict(X_test)

    verdaderos_positivos, falsos_negativos, falsos_positivos, verdaderos_negativos = matriz_de_confusion_y_reportar(
        evaluacion, y_test, y_pred)
