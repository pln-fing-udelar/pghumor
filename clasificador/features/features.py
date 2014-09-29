from __future__ import absolute_import

import clasificador.features.jergasexual
import clasificador.features.oov
import clasificador.features.primerapersona
import clasificador.features.presencia_animales
import clasificador.features.palabras_claves
from threading import Thread
from progress.bar import Bar

CANTIDAD_THREADS=4

class Features:
	def __init__(self):
		self.bar = ""
		self.features = {}
		for feature in [ \
				clasificador.features.jergasexual.JergaSexual(), \
				clasificador.features.oov.OOV(), \
				clasificador.features.primerapersona.PrimeraPersona(), \
				clasificador.features.presencia_animales.PresenciaAnimales(),\
				clasificador.features.palabras_claves.PalabrasClaves()\
				]:
			self.features[feature.nombre] = feature

	def calcular_features(self, tweets):
		intervalo = len(tweets)/CANTIDAD_THREADS
		threads = []
		for i in range(0,CANTIDAD_THREADS-1):
			t = Thread(target=self.calcular_features_thread, args=(tweets[i*intervalo: (i+1)*intervalo], i))
			threads.append(t)

		t = Thread(target=self.calcular_features_thread, args=(tweets[(CANTIDAD_THREADS - 1)*intervalo:], CANTIDAD_THREADS - 1))
		threads.append(t)
		self.bar = Bar('Calculando features ', max=len(tweets) * len(self.features), suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
		self.bar.next(0)

		for hilo in threads:
			hilo.start()

		for hilo in threads:
			hilo.join()

	def calcular_feature(self, tweets, nombre_feature):
		intervalo = len(tweets)/CANTIDAD_THREADS
		threads = []
		for i in range(0, CANTIDAD_THREADS-1):
			t = Thread(target=self.calcular_feature_thread, args=(tweets[i*intervalo:(i+1)*intervalo], nombre_feature, i))
			threads.append(t)

		t = Thread(target=self.calcular_feature_thread, args=(tweets[(CANTIDAD_THREADS - 1)*intervalo:], nombre_feature, CANTIDAD_THREADS - 1))
		threads.append(t)
		self.bar = Bar('Calculando feature ',  max=len(tweets), suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
		self.bar.next(0)
		for hilo in threads:
			hilo.start()

		for hilo in threads:
			hilo.join()

	def calcular_features_thread(self, tweets, identificador):

		for tweet in tweets:
			for feature in self.features.values():
				feature.calcular_feature(tweet)
				self.bar.next()
		self.bar.finish()

	def calcular_feature_thread(self, tweets, nombre_feature, identificador):

		for tweet in tweets:
			self.features[nombre_feature].calcular_feature(tweet)
			self.bar.next()
		self.bar.finish()
