# coding=utf-8
from __future__ import absolute_import, unicode_literals

import unittest

import clasificador.features.preguntasrespuestas
from clasificador.realidad.tweet import Tweet


class TestPreguntasRespuestas(unittest.TestCase):
    def test_preguntasrespuestas_basico(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = '¿De qué color era el caballo blanco de Artigas? Blanco.'
        tweet.texto_original = tweet.texto
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        preguntasrespuestas = clasificador.features.preguntasrespuestas.PreguntasRespuestas()

        tweet.features[preguntasrespuestas.nombre] = preguntasrespuestas.calcular_feature(tweet)
        self.assertEquals(1, tweet.features[preguntasrespuestas.nombre],
                          'El tweet debería tener 1 en preguntas-respuestas, no ' + str(tweet.features[
                              preguntasrespuestas.nombre]))

    def test_preguntasrespuestas_basico2(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = '-¿Qué te duele? -La mano -¿Por qué? -De tanto pensar en ti -¡Asqueroso! -Perdón, entonces no te vuelvo hacer una carta :('
        tweet.texto_original = tweet.texto
        tweet.favoritos = 75
        tweet.retweets = 113
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        preguntasrespuestas = clasificador.features.preguntasrespuestas.PreguntasRespuestas()

        tweet.features[preguntasrespuestas.nombre] = preguntasrespuestas.calcular_feature(tweet)
        self.assertEquals(2, tweet.features[preguntasrespuestas.nombre],
                          'El tweet debería tener 2 preguntas-respuestas, no ' + str(tweet.features[
                              preguntasrespuestas.nombre]))


if __name__ == '__main__':
    unittest.main()
