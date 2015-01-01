# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from clasificador.features.oov import contiene_caracteres_no_espanoles


class TestOOV(unittest.TestCase):
    def test_caracteres_no_espanoles_ascii(self):
        texto = "hola"
        self.assertFalse(contiene_caracteres_no_espanoles(texto),
                         "Deberían ser todos los caracteres españoles en el texto \"" + texto + "\"")

    def test_caracteres_no_espanoles_espanol(self):
        texto = "ñandú"
        self.assertFalse(contiene_caracteres_no_espanoles(texto),
                         "Deberían ser todos los caracteres españoles en el texto \"" + texto + "\"")

    def test_caracteres_no_espanoles_euro(self):
        texto = "€"
        self.assertTrue(contiene_caracteres_no_espanoles(texto),
                        "Deberían haber caracteres no españoles en el texto \"" + texto + "\"")


if __name__ == '__main__':
    unittest.main()
