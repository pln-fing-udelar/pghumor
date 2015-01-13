# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from clasificador.features.oov import contiene_caracteres_no_espanoles, eliminar_underscores, esta_en_google


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

    def test_esta_en_google_palabra_comun(self):
        texto = "hola"
        self.assertTrue(esta_en_google(texto), "Debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_palabra_comun_con_acento(self):
        texto = "árbol"
        self.assertTrue(esta_en_google(texto), "Debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_error_de_tipeo(self):
        texto = "holaa"
        self.assertFalse(esta_en_google(texto), "No debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_palabra_inexistente(self):
        texto = "jajajajaaaaaaaa"
        self.assertFalse(esta_en_google(texto), "No debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_palabra_inexistente2(self):
        texto = "aldnkvnvrbyweruvnrhuvhuirbv"
        self.assertFalse(esta_en_google(texto), "No debería estar en google el texto \"" + texto + "\"")

    def test_eliminar_underscore(self):
        texto = "hola_si"
        self.assertEquals("hola si", eliminar_underscores(texto),
                          "No se eliminaron los guíones bajos correctamente del texto \"" + texto + "\"")


if __name__ == '__main__':
    unittest.main()
