from __future__ import absolute_import

import subprocess


def obtener_diccionario(filename):
    lines = [line.rstrip('\n') for line in open(filename)]
    return lines


def ejecutar_comando(command):
    exito = False
    while not exito:
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            retorno = p.stdout.readlines()
            exito = True
        except:
            pass

    return retorno


def escapar(texto):
    return texto.replace('"', '\\"').replace("'", "\\'").replace("`", "\\`")
