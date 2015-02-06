#!/usr/bin/env python2
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

from progress.bar import IncrementalBar


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.define import SUFIJO_PROGRESS_BAR
import clasificador.herramientas.utils

if __name__ == "__main__":
    largo = 1000

    bar = IncrementalBar('Calculando', max=largo, suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)

    for i in range(largo):
        clasificador.herramientas.utils.ejecutar_comando("echo 1")
        bar.next()

    bar.finish()
