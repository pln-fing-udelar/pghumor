import jergasexual
import oov

class Features:
	
	def __init__(self):
		self.features = [
			jergasexual.JergaSexual(),
			oov.OOV(),
		]

	def calcularFeatures(self, tweets):
		for feature in self.features:
			for tweet in tweets:
				feature.calcularFeature(tweet)
