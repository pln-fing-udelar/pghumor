# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

import clasificador.features.palabrasmayusculas
from clasificador.realidad.tweet import Tweet


class TestPalabrasMayusculas(unittest.TestCase):
    def test_palabrasmayusculas_basico_con_acento_y_numeros(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = """Típico :
            –¿MAMÁ?
            –¿Qué?
            –Te amo
            –¡YA TE DIJE 2 VECES QUE NO VAS A SALIR!"""
        tweet.texto_original = tweet.texto
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        palabrasmayusculas = clasificador.features.palabrasmayusculas.PalabrasMayusculas()

        tweet.features[palabrasmayusculas.nombre] = palabrasmayusculas.calcular_feature(tweet)

        valor_esperado = 10 / 15

        self.assertEquals(valor_esperado, tweet.features[palabrasmayusculas.nombre],
                          "El tweet debería tener " + str(valor_esperado) + " en PalabrasMayusculas, no "
                          + str(tweet.features[palabrasmayusculas.nombre]))


if __name__ == '__main__':
    unittest.main()
