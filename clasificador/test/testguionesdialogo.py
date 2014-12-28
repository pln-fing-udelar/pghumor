# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import re
import unittest

from clasificador.features.preguntasrespuestas import guion_dialogo_re


class TestGuionesDialogo(unittest.TestCase):
    def test_captura_guion_clasico(self):
        patron = re.compile(r'^' + guion_dialogo_re() + r'$', re.UNICODE)
        self.assertIsNotNone(patron.match('-'), "Debería capturar el guión clásico")

if __name__ == '__main__':
    unittest.main()
