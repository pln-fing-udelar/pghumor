
from JergaSexual import *
from OOV import *


class Features:
	
	def __init__(self):
		self.features = []

		self.features.append(JergaSexual())
		self.features.append(OOV())	

	def calcularFeatures(self, tweets):

		for feature in self.features:
			for tweet in tweets:
				feature.calcularFeature(tweet)