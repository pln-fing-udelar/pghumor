# coding=utf-8
from __future__ import absolute_import, unicode_literals

from pkg_resources import resource_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from clasificador.features.feature import  Feature
from clasificador.herramientas.persistencia import *
from clasificador.herramientas.utils import *


def get_stop_words():
    return obtener_diccionario(resource_filename('clasificador.recursos.diccionarios', 'stop_words.txt'))


class DistanciaCategoria(Feature):

    def __init__(self, id_categoria, nombre_categoria, verbose):
        super(DistanciaCategoria, self).__init__()
        self.nombre = "DistanciaCategoria: " + nombre_categoria
        self.descripcion = """
            Mide la distancia utilizando bag of words entre la categoria""" + nombre_categoria + """ de chistes.com.
            y textos de no humor como son los encontrados en wikipedia
        """
        chistes = obtener_chistes_categoria(id_categoria)

        x_train = [chistes[i].texto_chiste for i in range(len(chistes))]
        y_train = [chistes[i].nombre_clasificacion for i in range(len(chistes))]

        stop_words = get_stop_words()

        documentos_wikicorpus = obtener_sample_wikicorpus()
        nuevo_x_train = x_train + documentos_wikicorpus
        nuevo_y_train = y_train + [u'wiki' for i in range(0, len(documentos_wikicorpus))]

        self.clf_4 = Pipeline([
            ('vect', TfidfVectorizer(
                stop_words=stop_words,
                token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b",
            )),
            ('clf', MultinomialNB(alpha=0.01)),
        ])

        self.clf_4.fit(nuevo_x_train, nuevo_y_train)

        self.verbose = verbose

    def calcular_feature(self, tweet):

        result = self.clf_4.predict_proba([tweet.texto_original])
        retorno = 0
        if self.verbose:
            print("El resultado es:")

        for i in range(0, len(result[0])):
            if self.clf_4.steps[1][1].classes_[i] != 'wiki':
                retorno = result[0][i]
            if self.verbose:
                print self.clf_4.steps[1][1].classes_[i], ": ", result[0][i]

        return retorno