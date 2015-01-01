# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from clasificador.herramientas.freeling import Freeling
from clasificador.realidad.tweet import Tweet


class TestFreeling(unittest.TestCase):
    def test_freeling_escapar(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = "3 Cosas que he aprendi en la escuela: Enviar WhatsApp's sin mirar. Dormir sin que me vean." \
                      + " El trabajo en equipo durante los exámenes."
        tweet.texto_original = tweet.texto
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        freeling = Freeling(tweet)
        self.assertNotEqual(freeling.tokens, [], "Error de tokens vacíos")


if __name__ == '__main__':
    unittest.main()
