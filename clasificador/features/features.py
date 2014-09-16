from __future__ import absolute_import

import clasificador.features.jergasexual
import clasificador.features.oov
import clasificador.features.primerapersona


class Features:
	def __init__(self):
		self.features = {}
		for feature in [ \
				clasificador.features.jergasexual.JergaSexual(), \
				clasificador.features.oov.OOV(), \
				clasificador.features.primerapersona.PrimeraPersona(), \
				]:
			self.features[feature.nombre] = feature

	def calcular_features(self, tweets):
		for feature in self.features.values():
			for tweet in tweets:
				feature.calcular_feature(tweet)

	def calcular_feature(self, tweets, nombre_feature):
		for tweet in tweets:
			self.features[nombre_feature].calcular_feature(tweet)
