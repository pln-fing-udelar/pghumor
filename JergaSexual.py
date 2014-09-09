
import Feature
import utils
import tokenizacion
import define
import utils

FEATURE_NAME="Jerga Sexual"

class JergaSexual(Feature.Feature):
	def __init__(self):
		self.palabrasSexuales = utils.obtenerDiccionario(define.PATH_DICCIONARIO_SEXUAL)
		
	def calcularFeature(self, tweet):

		valorFeature = 0

		tokens = tokenizacion.tokenizar(tweet.texto)

		print tokens

		tweet.features[FEATURE_NAME] = valorFeature