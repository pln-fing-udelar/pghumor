# coding=utf-8
import re
import unittest

from clasificador.features.preguntasrespuestas import guion_dialogo_re


class TestGuionesDialogo(unittest.TestCase):
    def test_captura_guion_clasico(self):
        patron = re.compile(ur'^' + guion_dialogo_re() + ur'$', re.UNICODE)
        self.assertIsNotNone(patron.match(u"-"), "Debería capturar el guión clásico")

if __name__ == '__main__':
    unittest.main()
