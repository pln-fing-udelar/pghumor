# coding=utf-8
import unittest

import clasificador.features.preguntarespuesta
from clasificador.realidad.tweet import Tweet


class TestPreguntaRespuesta(unittest.TestCase):
    def test_preguntarespuesta_basico(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = u'¿De qué color era el caballo blanco de Artigas? Blanco.'
        tweet.texto_original = tweet.texto
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        preguntarespuesta = clasificador.features.preguntarespuesta.PreguntaRespuesta()

        preguntarespuesta.calcular_feature(tweet)
        self.assertTrue(tweet.features[preguntarespuesta.nombre], 'El tweet debería ser pregunta-respuesta.')

if __name__ == '__main__':
    unittest.main()
