# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import unittest

from clasificador.herramientas.reflection import paquete, subclases, modulos_vecinos


class TestUtilReflection(unittest.TestCase):
    def test_paquete_basico(self):
        _paquete = paquete(__name__)
        self.assertEquals('.', _paquete, "El nombre de paquete debería ser '.' en lugar de " + _paquete)

    def test_subclases_basico(self):
        self.assertTrue(TestUtilReflection in subclases(unittest.TestCase))

    def test_modulos_vecinos_basico(self):
        self.assertTrue('testantonimos' in modulos_vecinos(__file__))


if __name__ == '__main__':
    unittest.main()
