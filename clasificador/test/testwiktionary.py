# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from clasificador.herramientas.wiktionary import Wiktionary


class TestWiktionary(unittest.TestCase):
    def test_esta_en_wiktionary_consulta_palabra_comun(self):
        texto = "hola"
        self.assertTrue(Wiktionary.pertenece_consulta(texto), "Debería estar en wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_consulta_palabra_comun_con_acento(self):
        texto = "árbol"
        self.assertTrue(Wiktionary.pertenece_consulta(texto), "Debería estar en wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_consulta_error_de_tipeo(self):
        texto = "holaa"
        self.assertFalse(Wiktionary.pertenece_consulta(texto), "No debería estar en wiktionary el texto \"" + texto
                         + "\"")

    def test_esta_en_wiktionary_consulta_palabra_inexistente(self):
        texto = "jajajajaaaaaaaa"
        self.assertFalse(Wiktionary.pertenece_consulta(texto), "No debería estar en wiktionary el texto \"" + texto
                         + "\"")

    def test_esta_en_wiktionary_consulta_palabra_inexistente2(self):
        texto = "aldnkvnvrbyweruvnrhuvhuirbv"
        self.assertFalse(Wiktionary.pertenece_consulta(texto), "No debería estar en wiktionary el texto \"" + texto
                         + "\"")

    def test_esta_en_wiktionary_consulta_palabra_cotidiana(self):
        texto = "Suárez"
        self.assertTrue(Wiktionary.pertenece_consulta(texto), "Debería estar en wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_palabra_comun(self):
        texto = "hola"
        self.assertTrue(Wiktionary.pertenece(texto),
                        "Debería estar en el diccionario de wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_palabra_comun_con_acento(self):
        texto = "árbol"
        self.assertTrue(Wiktionary.pertenece(texto),
                        "Debería estar en el diccionario de wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_error_de_tipeo(self):
        texto = "holaa"
        self.assertFalse(Wiktionary.pertenece(texto),
                         "No debería estar el diccionario de en wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_palabra_inexistente(self):
        texto = "jajajajaaaaaaaa"
        self.assertFalse(Wiktionary.pertenece(texto),
                         "No debería estar el diccionario de en wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_palabra_inexistente2(self):
        texto = "aldnkvnvrbyweruvnrhuvhuirbv"
        self.assertFalse(Wiktionary.pertenece(texto),
                         "No debería estar el diccionario de en wiktionary el texto \"" + texto + "\"")

    def test_esta_en_wiktionary_palabra_cotidiana(self):
        texto = "Suárez"
        self.assertTrue(Wiktionary.pertenece(texto), "Debería estar en wiktionary el texto \"" + texto + "\"")


if __name__ == '__main__':
    unittest.main()
