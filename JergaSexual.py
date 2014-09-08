
import Feature

FEATURE_NAME="Jerga Sexual"

class JergaSexual(Feature):
	def __init__(self):
		pass

	def calcularFeature(self, tweet):
		valorFeature = 0

		tweet.features[FEATURE_NAME] = valorFeature