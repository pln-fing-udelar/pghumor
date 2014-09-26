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
			t = Thread(target=self.calcular_features_thread, args=(tweets, i, i*intervalo, (i+1)*intervalo))
			threads.append(t)

		t = Thread(target=self.calcular_features_thread, args=(tweets, CANTIDAD_THREADS, (CANTIDAD_THREADS - 1)*intervalo, len(intervalo)))
		threads.append(t)

		for hilo in threads:
			hilo.start()

		for hilo in threads:
			hilo.join()

	def calcular_feature(self, tweets, nombre_feature):
		intervalo = len(tweets)/CANTIDAD_THREADS
		print intervalo
		threads = []
		for i in range(0, CANTIDAD_THREADS-1):
			print i, " - ", (i+1)*intervalo
			t = Thread(target=self.calcular_feature_thread, args=(tweets, nombre_feature, i, i*intervalo, (i+1)*intervalo))
			threads.append(t)

		print (CANTIDAD_THREADS - 1)*intervalo, " - ", len(tweets)
		t = Thread(target=self.calcular_feature_thread, args=(tweets, nombre_feature, CANTIDAD_THREADS, (CANTIDAD_THREADS - 1)*intervalo, len(tweets)))
		threads.append(t)

		for hilo in threads:
			hilo.start()

		for hilo in threads:
			hilo.join()

	def calcular_features_thread(self, tweets, identificador, ini, fin):
		bar = Bar('Calculando features ' + str(identificador), max=len(tweets) * len(self.features), suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
		bar.next(0)
		for i in range(ini,fin):
			for feature in self.features.values():
				feature.calcular_feature(tweets[i])
				bar.next()
		bar.finish()

	def calcular_feature_thread(self, tweets, nombre_feature, identificador, ini, fin):
		bar = Bar('Calculando feature ' + str(identificador),  max=fin-ini, suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
		bar.next(0)
		for i in range(ini, fin):
			self.features[nombre_feature].calcular_feature(tweets[i])
			bar.next()
		bar.finish()
