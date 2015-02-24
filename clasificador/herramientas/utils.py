# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import math
import subprocess

from pkg_resources import resource_filename


def ejecutar_comando(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    p.wait()
    return [linea.decode('utf-8') for linea in p.stdout.readlines()]


def eliminar_underscores(texto):
    return texto.replace('_', ' ')


def filtrar_segun_votacion(corpus):
    res = set()
    for tweet in corpus:
        if tweet.es_humor:
            if tweet.votos > 0:
                porcentaje_humor = tweet.votos_humor / float(tweet.votos)
                if porcentaje_humor >= 0.60:
                    res.add(tweet)
                elif porcentaje_humor <= 0.30:
                    tweet.es_humor = False
                    res.add(tweet)
        else:
            res.add(tweet)
    return res


def get_stop_words():
    with open(resource_filename('clasificador.recursos.diccionarios', 'stopwords.dic')) as archivo:
        return {linea.strip() for linea in archivo}


def obtener_diccionario(filename):
    with open(filename) as archivo:
        return {linea.decode('utf-8').rstrip('\n') for linea in archivo if linea.decode('utf-8').rstrip('\n')}


def entropia(p):
    """Entropía de una Bernoulli de parámetro p."""
    if p == 0 or p == 1:
        return 0
    else:
        return - p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)


def distancia_edicion(s1, s2):
    if len(s1) < len(s2):
        return distancia_edicion(s2, s1)

    if len(s2) == 0:
        return len(s1)

    fila_anterior = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        fila_actual = [i + 1]
        for j, c2 in enumerate(s2):
            inserciones = fila_anterior[j + 1] + 1
            eliminaciones = fila_actual[j] + 1
            sustituciones = fila_anterior[j] + (c1 != c2)
            fila_actual.append(min(inserciones, eliminaciones, sustituciones))
        fila_anterior = fila_actual

    return fila_anterior[-1]
