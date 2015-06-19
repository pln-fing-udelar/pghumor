# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from threading import Thread

from progress.bar import Bar

import clasificador.features.distanciacategoria
from clasificador.features.feature import Feature
import clasificador.features.npersona
import clasificador.herramientas.chistesdotcom
from clasificador.herramientas.define import SUFIJO_PROGRESS_BAR
import clasificador.herramientas.persistencia
from clasificador.herramientas.reflection import cargar_modulos_vecinos, subclases


class Features:
    def __init__(self, cantidad_threads):
        self.cantidad_threads = cantidad_threads
        self.bar = ""
        self.features = {}

        print("Comienzo de la carga de caracteristicas")

        cargar_modulos_vecinos(__name__, __file__)

        for clase_feature in subclases(Feature):
            if clase_feature != clasificador.features.distanciacategoria.DistanciaCategoria \
                    and clase_feature != clasificador.features.npersona.NPersona:
                objeto_feature = clase_feature()
                if objeto_feature.incluir:
                    self.features[objeto_feature.nombre] = objeto_feature
                    #print(objeto_feature.nombre)

        categorias_chistes_dot_com = clasificador.herramientas.chistesdotcom.obtener_categorias()

        for categoria in categorias_chistes_dot_com:
            feature = clasificador.features.distanciacategoria.DistanciaCategoria(categoria['id_clasificacion'],
                                                                                  categoria['nombre_clasificacion'],
                                                                                  False)
            if feature.incluir:
                self.features[feature.nombre] = feature
                print(feature.nombre)

        print("Fin de la carga de caracteristicas")

    def abortar_si_feature_no_es_thread_safe(self, feature):
        assert self.cantidad_threads == 1 or feature.thread_safe, \
            "La feature " + feature.nombre + " no es thread-safe y hay más de un hilo corriendo"

    def calcular_features(self, tweets):
        self.repartir_en_threads_PRUEBA(self.calculoFeaturePOSIX, tweets)

    def calcular_feature(self, tweets, nombre_feature):
        self.repartir_en_threads(self.calcular_feature_thread, tweets, nombre_feature)

    def calcular_features_faltantes(self, tweets):
        self.repartir_en_threads(self.calcular_features_faltantes_thread, tweets)

    def repartir_en_threads(self, funcion, tweets, nombre_feature=None):
        intervalo = int(len(tweets) / self.cantidad_threads)
        threads = []
        for i in range(self.cantidad_threads - 1):
            if nombre_feature:
                args = (tweets[i * intervalo: (i + 1) * intervalo], nombre_feature, i)
            else:
                args = (tweets[i * intervalo: (i + 1) * intervalo], i)
            thread = Thread(target=funcion, args=args)
            threads.append(thread)

        if nombre_feature:
            args = (tweets[(self.cantidad_threads - 1) * intervalo:], nombre_feature, self.cantidad_threads - 1)
        else:
            args = (tweets[(self.cantidad_threads - 1) * intervalo:], self.cantidad_threads - 1)
        thread = Thread(target=funcion, args=args)
        threads.append(thread)

        for hilo in threads:
            hilo.start()

        for hilo in threads:
            hilo.join()



    def calculoFeaturePOSIX(self, tweets, feature):
        print("calculando feature" + feature.nombre)
        feature.calcular_feature_prueba_tweets(tweets)


    def repartir_en_threads_PRUEBA(self, funcion, tweets):
        intervalo = int(len(tweets) / self.cantidad_threads)
        threads = []
        for feature in list(self.features.values()):
            args = (tweets, feature)
            thread = Thread(target=funcion, args=args)
            threads.append(thread)

        for hilo in threads:
            hilo.start()

        for hilo in threads:
            hilo.join()

    def calcular_features_thread(self, tweets, identificador):
        if len(tweets) > 0:
            bar = Bar("Calculando features - " + unicode(identificador), max=len(tweets) * len(self.features),
                      suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)
            for tweet in tweets:
                for feature in list(self.features.values()):
                    self.abortar_si_feature_no_es_thread_safe(feature)
                    tweet.features[feature.nombre] = feature.calcular_feature(tweet)
                    bar.next()
            bar.finish()

   #funcion declarada peligrosa
    def calcular_features_thread_PRUEBA(self, tweets, identificador):
        if len(tweets) > 0:
            bar = Bar("Calculando features - " + unicode(identificador), max=len(tweets) * len(self.features),
                      suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)
            for feature in list(self.features.values()):
                self.abortar_si_feature_no_es_thread_safe(feature)
                feature.calcular_feature_prueba_tweets(tweets)
                bar.next()
            bar.finish()

    def calcular_feature_thread(self, tweets, nombre_feature, identificador):
        if len(tweets) > 0:
            bar = Bar("Calculando feature " + nombre_feature + ' - ' + unicode(identificador),
                      max=len(tweets),
                      suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)
            feature = self.features[nombre_feature]
            self.abortar_si_feature_no_es_thread_safe(feature)
            for tweet in tweets:
                tweet.features[feature.nombre] = feature.calcular_feature(tweet)
                bar.next()
            bar.finish()

    def calcular_features_faltantes_thread(self, tweets, identificador):
        if len(tweets) > 0:
            bar = Bar("Calculando features - " + unicode(identificador), max=len(tweets) * len(self.features),
                      suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)
            for tweet in tweets:
                for feature in list(self.features.values()):
                    self.abortar_si_feature_no_es_thread_safe(feature)
                    if feature.nombre not in tweet.features:
                        tweet.features[feature.nombre] = feature.calcular_feature(tweet)
                    bar.next()
            bar.finish()
