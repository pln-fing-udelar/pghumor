#!/usr/bin/env python
import csv
import sys
import time
import tweepy

from clasificador.herramientas.define import *
from clasificador.herramientas.tokenizacion import *
import clasificador.herramientas.utils

from pkg_resources import resource_filename


def main():
	dic = bootstrap()
	guardar_diccionario(dic)


def bootstrap():
	global tweets
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)

	api = tweepy.API(auth)

	palabras_sexuales = clasificador.herramientas.utils.obtener_diccionario(
		resource_filename('clasificador.recursos.diccionarios', 'DiccionarioSexual.txt'))

	bootstrapping = {}
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
						print("Ocurrio un error ." + "Haciendo el intento numero " + str(reintentos) + ".")

				for tweet in tweets:
					for oracion in tokenizar(tweet.text):
						for palabra in oracion:
							incrementar_key(bootstrapping, palabra, palabras_sexuales)

	return bootstrapping


def incrementar_key(dicc, key, exluidas):
	if key.lower() not in exluidas:
		if key in dicc:
			dicc[key] += 1
		else:
			dicc[key] = 1


def guardar_diccionario(dicc):
	w = csv.writer(open("diccSexo.csv", "w"))
	for key, val in dicc.items():
		w.writerow([key.encode('utf-8'), val])


def cargar_diccionario(path):
	retorno = {}
	with open(path, 'rb') as f:
		mycsv = csv.reader(f)
		for row in mycsv:
			retorno[row[0].decode('utf-8')] = int(row[1])

	return retorno


def imprimir_top(dicc, top):
	i = 0
	for w in sorted(dicc, key=dicc.get, reverse=True):
		i += 1
		if i > top:
			break
		print w, dicc[w]


def pulcrar_dic(dicc):
	for key, value in dicc.items():
		if len(key) < 4:
			del dicc[key]


def clasificar(dicc):
	retorno = []
	for w in sorted(dicc, key=dicc.get, reverse=True):
		print w, dicc[w]
		clasificacion = sys.stdin.readline()
		if clasificacion != '\n':
			retorno.append(w)
		if clasificacion == 'f\n':
			break

	return retorno


def guardar_dicc_para_feature(palabrasSexuales):
	file_object = open(resource_filename('clasificador.recursos.diccionarios', 'DiccionarioSexual.txt'), 'a')

	for word in palabrasSexuales:
		file_object.write(word + "\n")

	file_object.close()
