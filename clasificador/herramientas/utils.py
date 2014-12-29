# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import subprocess


def obtener_diccionario(filename):
    with open(filename) as archivo:
        return [linea.decode('utf-8').rstrip('\n') for linea in archivo]


def ejecutar_comando(command):
    while True:
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            return [linea.decode('utf-8') for linea in p.stdout.readlines()]
        except:
            # FIXME: habría que tomar una excepción más específica, ya que
            # no se puede salir por Ctrl + C del programa si está acá
            pass
