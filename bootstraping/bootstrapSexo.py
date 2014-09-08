#!/usr/bin/env python

import tweepy
import sys
import csv

sys.path.append("../")
from utils import *
from define import *
from tokenizacion import *


def main():
	dic = bootstrap()
	guardarDiccionario(dic)

def bootstrap():

	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)

	api = tweepy.API(auth)


	palabrasSexuales = obtenerDiccionario("../" +PATH_DICCIONARIO_SEXUAL)

	bootstrapping = {}
	i = 0
	for palabra1 in palabrasSexuales:
		for palabra2 in palabrasSexuales:
			if palabra1 != palabra2:			
				
				print "Buscando: " + palabra1 + " - " + palabra2

				query = palabra1 + " " + palabra2
				reintentos = 0
				exito = False
				while reintentos < 3 and not exito:
					try:
						tweets = api.search(q=query)
						exito = True
					except Exception:
						reintentos = reintentos + 1
						print "Ocurrio un error ." + "Haciendo el intento numero " + `reintentos` + "."


				for tweet in tweets:
					for oracion in tokenizar(tweet.text):
						for palabra in oracion:		
							incrementarKey(bootstrapping, palabra)


	return bootstrapping

def incrementarKey(dicc, key):
	if key in dicc:
		dicc[key] = dicc[key] + 1
	else:
		dicc[key] = 1

def guardarDiccionario(dicc):
	w = csv.writer(open("diccSexo.csv", "w"))
	for key, val in dicc.items():
		w.writerow([key.encode('utf-8'), val])

def cargarDiccionario(path):
	retorno = {}
	with open(path, 'rb') as f:
		mycsv = csv.reader(f)
		for row in mycsv:
			retorno[row[0].decode('utf-8')] = int(row[1])

	return retorno

def imprimirTop(dicc, top):
	
	i = 0
	for w in sorted(dicc, key=dicc.get, reverse=True):
  		i = i+ 1
  		if i > top:
  			break
  		print w, dicc[w]

def pulcrarDic(dicc):
	for key, value in dicc.items():
		if (len(key) < 4):
			del dicc[key]

def clasificar(dicc):
	retorno = []
	for w in sorted(dicc, key=dicc.get, reverse=True):
  		print w, dicc[w]
  		clasificacion = sys.stdin.readline()
  		if clasificacion != '\n':
  			retorno.append(w)

  	return retorno