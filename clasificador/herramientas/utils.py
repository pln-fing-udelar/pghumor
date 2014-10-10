from __future__ import absolute_import

import subprocess


def obtener_diccionario(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    return lines


def ejecutar_comando(command):
    while True:
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            return p.stdout.readlines()
        except:
            pass


def escapar(texto):
    return texto.replace('"', '\\"').replace("'", "\\'").replace("`", "\\`")
