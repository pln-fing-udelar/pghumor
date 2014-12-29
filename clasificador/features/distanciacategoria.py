# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from pkg_resources import resource_filename

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

from clasificador.features.feature import Feature
from clasificador.herramientas.chistesdotcom import obtener_chistes_categoria
from clasificador.herramientas.utils import *
from clasificador.herramientas.wikicorpus import obtener_sample_wikicorpus


def get_stop_words():
    return obtener_diccionario(resource_filename('clasificador.recursos.diccionarios', 'stop_words.txt'))


class DistanciaCategoria(Feature):
    def __init__(self, id_categoria, nombre_categoria, verbose):
        super(DistanciaCategoria, self).__init__()
        self.nombre = "DistanciaCategoria: " + nombre_categoria
        self.descripcion = """
            Mide la distancia utilizando Bag Of Words entre la categoria """ + nombre_categoria + """ de chistes.com
            y textos de no humor como son los encontrados en wikipedia.
        """
        chistes = obtener_chistes_categoria(id_categoria)

        features = [chiste.texto_chiste for chiste in chistes]
        clases = [chiste.nombre_clasificacion for chiste in chistes]

        documentos_wikicorpus = obtener_sample_wikicorpus()
        nuevas_features = features + documentos_wikicorpus
        nuevas_clases = clases + ['wiki' for _ in documentos_wikicorpus]

        self.clasificador = Pipeline([
            ('vect', TfidfVectorizer(
                stop_words=get_stop_words(),
                token_pattern=r'\b[a-z0-9_\-\.]+[a-z][a-z0-9_\-\.]+\b',
            )),
            ('clf', MultinomialNB(alpha=0.01)),
        ])

        self.clasificador.fit(nuevas_features, nuevas_clases)

        self.verbose = verbose

    def calcular_feature(self, tweet):
        result = self.clasificador.predict_proba([tweet.texto_original])
        retorno = 0
        if self.verbose:
            print("El resultado es:")

        for i in range(len(result[0])):
            if self.clasificador.steps[1][1].classes_[i] != 'wiki':
                retorno = result[0][i]
            if self.verbose:
                print(self.clasificador.steps[1][1].classes_[i], ": ", result[0][i])

        return retorno
