from __future__ import absolute_import

import clasificador.features.jergasexual
import clasificador.features.oov
import clasificador.features.primerapersona
import clasificador.features.presencia_animales
import clasificador.features.palabras_claves

from progress.bar import Bar


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
		bar = Bar('Calculando features', max=len(tweets) * len(self.features), suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
		bar.next(0)
		for tweet in tweets:
			for feature in self.features.values():
				feature.calcular_feature(tweet)
				bar.next()
		bar.finish()

	def calcular_feature(self, tweets, nombre_feature):
		bar = Bar('Calculando feature',  max=len(tweets) * len(self.features), suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
		bar.next(0)
		for tweet in tweets:
			self.features[nombre_feature].calcular_feature(tweet)
			bar.next()
		bar.finish()
