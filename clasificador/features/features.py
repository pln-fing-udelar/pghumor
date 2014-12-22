# coding=utf-8
from __future__ import absolute_import, unicode_literals

from threading import Thread

from progress.bar import Bar

import clasificador.features.antonimos
import clasificador.features.dialogo
import clasificador.features.exclamacion
import clasificador.features.hashtags
import clasificador.features.jergasexual
import clasificador.features.links
import clasificador.features.oov
import clasificador.features.palabrasclave
import clasificador.features.preguntasrespuestas
import clasificador.features.presenciaanimales
import clasificador.features.primerapersona
import clasificador.features.segundapersona
import clasificador.features.distanciacategoria
import clasificador.herramientas.persistencia

CANTIDAD_THREADS = 1  # Cuidado que Antonimos tiene problemas de concurrencia


class Features:
    def __init__(self):
        self.bar = ""
        self.features = {}
        for feature in [
            clasificador.features.antonimos.Antonimos(),
            clasificador.features.dialogo.Dialogo(),
            clasificador.features.exclamacion.Exclamacion(),
            clasificador.features.hashtags.Hashtags(),
            clasificador.features.jergasexual.JergaSexual(),
            clasificador.features.links.Links(),
            clasificador.features.oov.OOV(),
            clasificador.features.palabrasclave.PalabrasClave(),
            clasificador.features.preguntasrespuestas.PreguntasRespuestas(),
            clasificador.features.presenciaanimales.PresenciaAnimales(),
            clasificador.features.primerapersona.PrimeraPersona(),
            clasificador.features.segundapersona.SegundaPersona(),
        ]:
            self.features[feature.nombre] = feature
            print('Cargada catacterística: ' + feature.nombre)

        categorias_chistes_dot_com = clasificador.herramientas.persistencia.obtener_categorias()

        for categoria in categorias_chistes_dot_com:
            feature = clasificador.features.distanciacategoria.DistanciaCategoria(categoria['id_clasificacion'],
                                                                                  categoria['nombre_clasificacion'],
                                                                                  False)
            self.features[feature.nombre] = feature

            print('Cargada catacterística: ' + feature.nombre)

        print('Fin cargar características')

    def calcular_features(self, tweets):
        intervalo = len(tweets) / CANTIDAD_THREADS
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
        intervalo = len(tweets) / CANTIDAD_THREADS
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
        intervalo = len(tweets) / CANTIDAD_THREADS
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
            # print("termino thread " + str(identificador))
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
            # print("Termino thread " + str(identificador))
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
            # print("termino thread " + str(identificador))
            bar.finish()
