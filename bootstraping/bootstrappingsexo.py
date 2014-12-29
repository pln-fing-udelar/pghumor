#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict
import csv
import os
import sys
import time

from pkg_resources import resource_filename
import tweepy


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.define import *
from clasificador.herramientas.tokenizacion import *
import clasificador.herramientas.utils


def main():
    dicc_palabras = bootstrapping()
    guardar_diccionario(dicc_palabras)


def bootstrapping():
    global tweets
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)

    api = tweepy.API(auth)

    palabras_sexuales = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'DiccionarioSexual.txt'))

    dicc_palabras = defaultdict(0)
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
                    except:
                        time.sleep(60)
                        reintentos += 1
                        print("Ocurrió un error haciendo el intento número " + str(reintentos) + ".")

                for tweet in tweets:
                    for oracion in tokenizar(tweet.text):
                        for palabra in oracion:
                            if palabra.lower() not in palabras_sexuales:
                                dicc_palabras[palabra] += 1
    return dicc_palabras


def guardar_diccionario(dicc):
    with open('diccSexo.csv', 'w') as archivo:
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
    for palabra in sorted(dicc, key=dicc.get, reverse=True)[:top]:
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
    with open(resource_filename('clasificador.recursos.diccionarios', 'DiccionarioSexual.txt'), 'a') as archivo:
        archivo.writelines(palabras_sexuales)
