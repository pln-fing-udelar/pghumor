# coding=utf-8
from __future__ import absolute_import, unicode_literals

import glob
import importlib
import os


def subclases(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in subclases(s)]


def paquete(module):
    return '.'.join(module.split('.')[:-1]) + '.'


def cargar_modulos_vecinos(modulo, archivo):
    _paquete = paquete(modulo)

    for archivo_python_vecino in glob.glob(os.path.dirname(archivo) + '/*.py'):
        if archivo_python_vecino != '__init__.py':
            modulo_vecino = os.path.basename(archivo_python_vecino)[:-3]
            importlib.import_module(_paquete + modulo_vecino)
