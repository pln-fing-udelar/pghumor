from __future__ import absolute_import

import clasificador.features.jergasexual
import clasificador.features.oov
import clasificador.features.primerapersona


class Features:
	def __init__(self):
		self.features = [
			clasificador.features.jergasexual.JergaSexual(),
			clasificador.features.oov.OOV(),
			clasificador.features.primerapersona.PrimeraPersona(),
		]

	def calcular_features(self, tweets):
		for feature in self.features:
			for tweet in tweets:
				feature.calcular_feature(tweet)
