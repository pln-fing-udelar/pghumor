# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from clasificador.herramientas.google import Google


class TestGoogle(unittest.TestCase):
    def test_esta_en_google_consulta_palabra_comun(self):
        texto = "hola"
        self.assertTrue(Google.esta_en_google_consulta(texto), "Debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_consulta_palabra_comun_con_acento(self):
        texto = "árbol"
        self.assertTrue(Google.esta_en_google_consulta(texto), "Debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_consulta_error_de_tipeo(self):
        texto = "holaa"
        self.assertFalse(Google.esta_en_google_consulta(texto), "No debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_consulta_palabra_inexistente(self):
        texto = "jajajajaaaaaaaa"
        self.assertFalse(Google.esta_en_google_consulta(texto), "No debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_consulta_palabra_inexistente2(self):
        texto = "aldnkvnvrbyweruvnrhuvhuirbv"
        self.assertFalse(Google.esta_en_google_consulta(texto), "No debería estar en google el texto \"" + texto + "\"")

    def test_esta_en_google_palabra_comun(self):
        texto = "hola"
        self.assertTrue(Google.esta_en_google(texto),
                        "Debería estar en el diccionario de google el texto \"" + texto + "\"")

    def test_esta_en_google_palabra_comun_con_acento(self):
        texto = "árbol"
        self.assertTrue(Google.esta_en_google(texto),
                        "Debería estar en el diccionario de google el texto \"" + texto + "\"")

    def test_esta_en_google_error_de_tipeo(self):
        texto = "holaa"
        self.assertFalse(Google.esta_en_google(texto),
                         "No debería estar el diccionario de en google el texto \"" + texto + "\"")

    def test_esta_en_google_palabra_inexistente(self):
        texto = "jajajajaaaaaaaa"
        self.assertFalse(Google.esta_en_google(texto),
                         "No debería estar el diccionario de en google el texto \"" + texto + "\"")

    def test_esta_en_google_palabra_inexistente2(self):
        texto = "aldnkvnvrbyweruvnrhuvhuirbv"
        self.assertFalse(Google.esta_en_google(texto),
                         "No debería estar el diccionario de en google el texto \"" + texto + "\"")


if __name__ == '__main__':
    unittest.main()
