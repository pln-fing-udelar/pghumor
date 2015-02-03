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
    res = []
    for tweet in corpus:
        if tweet.es_humor:
            if tweet.votos > 0:
                porcentaje_humor = tweet.votos_humor / float(tweet.votos)
                if porcentaje_humor >= 0.60:
                    res.append(tweet)
                elif porcentaje_humor <= 0.30:
                    tweet.es_humor = False
                    res.append(tweet)
        else:
            res.append(tweet)
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
