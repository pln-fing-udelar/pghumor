#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict
import csv
from heapq import nlargest
import os
import sys
import time

from pkg_resources import resource_filename
import tweepy


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.define import *
from clasificador.herramientas.tokenizacion import *
import clasificador.herramientas.utils


def bootstrapping():
    global tweets
    auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    api = tweepy.API(auth)

    palabras_sexuales = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'sexual.dic'))

    _dicc_palabras = defaultdict(int)
    for palabra1 in palabras_sexuales:
        for palabra2 in palabras_sexuales:
            if palabra1 != palabra2:
                print("Buscando: " + palabra1 + " - " + palabra2)

                query = palabra1 + " " + palabra2
                reintentos = 0
                exito = False
                while not exito:
                    try:
                        tweets = api.search(q=query)
                        exito = True
                    except KeyboardInterrupt:
                        raise
                    except Exception:
                        time.sleep(60)
                        reintentos += 1
                        print("Ocurrió un error haciendo el intento número {n_reintentos}.".format(n_reintentos=reintentos))

                for tweet in tweets:
                    for oracion in tokenizar(tweet.text):
                        for palabra in oracion:
                            if palabra.lower() not in palabras_sexuales:
                                _dicc_palabras[palabra] += 1
    return _dicc_palabras


def guardar_diccionario(dicc):
    with open(resource_filename('bootstrapping', 'diccSexo.csv'), 'w') as archivo:
        writer = csv.writer(archivo)
        for clave, valor in dicc.viewitems():
            writer.writerow([clave.encode('utf-8'), valor])


def cargar_diccionario(path):
    retorno = {}
    with open(path, 'rb') as archivo:
        for fila in csv.reader(archivo):
            retorno[fila[0].decode('utf-8')] = int(fila[1])
    return retorno


def imprimir_top(dicc, top):
    for palabra in nlargest(top, dicc, key=dicc.get):
        print(palabra, dicc[palabra])


def pulcrar(dicc):
    for palabra in dicc:
        if len(palabra) < 4:
            del dicc[palabra]


def clasificar(dicc):
    retorno = []
    for palabra in sorted(dicc, key=dicc.get, reverse=True):
        print(palabra, dicc[palabra])
        clasificacion = sys.stdin.readline()
        if clasificacion != '\n':
            retorno.append(palabra)
        if clasificacion == 'f\n':
            break
    return retorno


def guardar_dicc_para_feature(palabras_sexuales):
    with open(resource_filename('clasificador.recursos.diccionarios', 'sexual.dic'), 'a') as archivo:
        archivo.writelines(palabras_sexuales)


if __name__ == "__main__":
    dicc_palabras = bootstrapping()
    guardar_diccionario(dicc_palabras)
