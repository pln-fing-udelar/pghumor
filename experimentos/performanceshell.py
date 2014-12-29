#!/usr/bin/env python2
# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import os
import sys

from progress.bar import Bar


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import clasificador.herramientas.utils

if __name__ == "__main__":
    largo = 1000

    bar = Bar('Calculando', max=largo, suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
    bar.next(0)

    for i in range(largo):
        clasificador.herramientas.utils.ejecutar_comando("echo 1")
        bar.next()

    bar.finish()
