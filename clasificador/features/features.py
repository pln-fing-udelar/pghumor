# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from threading import Thread

from progress.bar import Bar

import clasificador.features.distanciacategoria
from clasificador.features.feature import Feature
import clasificador.features.npersona
import clasificador.herramientas.chistesdotcom
import clasificador.herramientas.persistencia
from clasificador.herramientas.reflection import cargar_modulos_vecinos, subclases

# Cuidado que Antonimos tiene problemas de concurrencia
# https://github.com/nltk/nltk/issues/803
CANTIDAD_THREADS = 4


class Features:
    def __init__(self):
        self.bar = ""
        self.features = {}

        cargar_modulos_vecinos(__name__, __file__)

        for clase_feature in subclases(Feature):
            if clase_feature != clasificador.features.distanciacategoria.DistanciaCategoria \
                    and clase_feature != clasificador.features.npersona.NPersona:
                objeto_feature = clase_feature()
                if objeto_feature.incluir:
                    self.features[objeto_feature.nombre] = objeto_feature
                    print('Cargada catacterística: ' + objeto_feature.nombre)

        categorias_chistes_dot_com = clasificador.herramientas.chistesdotcom.obtener_categorias()

        for categoria in categorias_chistes_dot_com:
            feature = clasificador.features.distanciacategoria.DistanciaCategoria(categoria['id_clasificacion'],
                                                                                  categoria['nombre_clasificacion'],
                                                                                  False)
            self.features[feature.nombre] = feature
            print('Cargada catacterística: ' + feature.nombre)

        print('Fin cargar características')

    def calcular_features(self, tweets):
        intervalo = int(len(tweets) / CANTIDAD_THREADS)
        threads = []
        for i in range(CANTIDAD_THREADS - 1):
            t = Thread(target=self.calcular_features_thread, args=(tweets[i * intervalo: (i + 1) * intervalo], i))
            threads.append(t)

        t = Thread(target=self.calcular_features_thread,
                   args=(tweets[(CANTIDAD_THREADS - 1) * intervalo:], CANTIDAD_THREADS - 1))
        threads.append(t)

        for hilo in threads:
            hilo.start()

        for hilo in threads:
            hilo.join()

    def calcular_feature(self, tweets, nombre_feature):
        intervalo = int(len(tweets) / CANTIDAD_THREADS)
        threads = []
        for i in range(CANTIDAD_THREADS - 1):
            t = Thread(target=self.calcular_feature_thread,
                       args=(tweets[i * intervalo:(i + 1) * intervalo], nombre_feature, i))
            threads.append(t)

        t = Thread(target=self.calcular_feature_thread,
                   args=(tweets[(CANTIDAD_THREADS - 1) * intervalo:], nombre_feature, CANTIDAD_THREADS - 1))
        threads.append(t)

        for hilo in threads:
            hilo.start()

        for hilo in threads:
            hilo.join()

    def calcular_features_faltantes(self, tweets):
        intervalo = int(len(tweets) / CANTIDAD_THREADS)
        threads = []
        for i in range(CANTIDAD_THREADS - 1):
            t = Thread(target=self.calcular_features_faltantes_thread,
                       args=(tweets[i * intervalo: (i + 1) * intervalo], i))
            threads.append(t)

        t = Thread(target=self.calcular_features_faltantes_thread,
                   args=(tweets[(CANTIDAD_THREADS - 1) * intervalo:], CANTIDAD_THREADS - 1))
        threads.append(t)

        for hilo in threads:
            hilo.start()

        for hilo in threads:
            hilo.join()

    def calcular_features_thread(self, tweets, identificador):
        if len(tweets) > 0:
            bar = Bar('Calculando features - ' + str(identificador), max=len(tweets) * len(self.features),
                      suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
            bar.next(0)
            for tweet in tweets:
                for feature in self.features.values():
                    tweet.features[feature.nombre] = feature.calcular_feature(tweet)
                    bar.next()
            bar.finish()

    def calcular_feature_thread(self, tweets, nombre_feature, identificador):
        if len(tweets) > 0:
            bar = Bar('Calculando feature ' + nombre_feature + ' - ' + str(identificador), max=len(tweets),
                      suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
            bar.next(0)
            feature = self.features[nombre_feature]
            for tweet in tweets:
                tweet.features[feature.nombre] = feature.calcular_feature(tweet)
                bar.next()
            bar.finish()

    def calcular_features_faltantes_thread(self, tweets, identificador):
        if len(tweets) > 0:
            bar = Bar('Calculando features - ' + str(identificador), max=len(tweets) * len(self.features),
                      suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
            bar.next(0)
            for tweet in tweets:
                for feature in self.features.values():
                    if feature.nombre not in tweet.features:
                        tweet.features[feature.nombre] = feature.calcular_feature(tweet)
                    bar.next()
            bar.finish()
