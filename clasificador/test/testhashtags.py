# coding=utf-8
from __future__ import unicode_literals

import unittest

import clasificador.features.hashtags
from clasificador.realidad.tweet import Tweet


class TestHashtags(unittest.TestCase):
    def test_hashtags_basico(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = '#cuatro Tweet #uno #doña que #tres #asdfAsfsdañaáéáuasdfasd hola'
        tweet.texto_original = tweet.texto
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        hashtags = clasificador.features.hashtags.Hashtags()

        tweet.features[hashtags.nombre] = hashtags.calcular_feature(tweet)
        self.assertEquals(5, tweet.features[hashtags.nombre],
                          'El tweet debería tener 5 hashtags, no ' + str(tweet.features[hashtags.nombre]))


if __name__ == '__main__':
    unittest.main()
