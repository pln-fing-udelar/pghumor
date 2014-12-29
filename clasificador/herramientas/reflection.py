# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import glob
import importlib
import os


def subclases(cls):
    return cls.__subclasses__() + [g for s in cls.__subclasses__()
                                   for g in subclases(s)]


def paquete(module):
    return '.'.join(module.split('.')[:-1]) + '.'


def archivos_python_vecinos(archivo):
    return glob.glob(os.path.dirname(archivo) + '/*.py')


def modulos_vecinos(archivo):
    return [os.path.basename(archivo_python_vecino)[:-3] for archivo_python_vecino in archivos_python_vecinos(archivo)]


def cargar_modulos_vecinos(modulo, archivo):
    _paquete = paquete(modulo)

    for modulo_vecino in modulos_vecinos(archivo):
        if modulo_vecino != '__init__':
            importlib.import_module(_paquete + modulo_vecino)
