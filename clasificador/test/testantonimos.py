# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import clasificador.features.antonimos
from clasificador.realidad.tweet import Tweet


class TestAntonimos(unittest.TestCase):
    def test_antonimos_basico(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = "Un pequeño paso para el hombre, pero es un gran paso para la humanidad."
        tweet.texto_original = tweet.texto
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        antonimos = clasificador.features.antonimos.Antonimos()

        tweet.features[antonimos.nombre] = antonimos.calcular_feature(tweet)
        self.assertEquals(0.25, tweet.features[antonimos.nombre],
                          "El tweet debería tener 0.25 en antonimos, no " + unicode(tweet.features[antonimos.nombre]))


if __name__ == '__main__':
    unittest.main()
