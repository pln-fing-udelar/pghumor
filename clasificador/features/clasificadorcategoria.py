# -*- coding: utf-8 -*-
from __future__ import  absolute_import, unicode_literals

import random

from pkg_resources import resource_filename
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from clasificador.herramientas.persistencia import *
from clasificador.herramientas.utils import *


def get_stop_words():
    return obtener_diccionario(resource_filename('clasificador.recursos.diccionarios', 'stop_words.txt'))


class ClasificadorCategoria:

    def __init__(self, id_categoria, verbose):
        chistes = obtener_chistes_categoria(id_categoria)

        x_train = [chistes[i].texto_chiste for i in range(len(chistes))]
        y_train = [chistes[i].nombre_clasificacion for i in range(len(chistes))]

        stop_words = get_stop_words()

        documentos = read_wiki_corpus()
        cantidad_documentos_wikicorpus = 1000

        sample_wikicorpus = random.sample(documentos, cantidad_documentos_wikicorpus)

        nuevo_x_train = x_train + sample_wikicorpus
        nuevo_y_train = y_train + ['wiki' for i in range(0, cantidad_documentos_wikicorpus)]
        self.clf_4 = Pipeline([
            ('vect', TfidfVectorizer(
                stop_words=stop_words,
                token_pattern=ur"\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b",
            )),
            ('clf', MultinomialNB(alpha=0.01)),
        ])

        self.clf_4.fit(nuevo_x_train, nuevo_y_train)

        self.verbose = verbose

    def testear(self, texto):

        result = self.clf_4.predict_proba([texto])
        retorno = 0
        if self.verbose:
            print("El resultado es:")

        for i in range(0, len(result[0])):
            if self.clf_4.steps[1][1].classes_[i] != 'wiki':
                retorno = result[0][i]
            if self.verbose:
                print self.clf_4.steps[1][1].classes_[i], ": ", result[0][i]

        return retorno