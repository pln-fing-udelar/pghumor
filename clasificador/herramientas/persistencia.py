from __future__ import absolute_import

import mysql.connector
from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME

from clasificador.realidad.tweet import Tweet


def cargar_tweets():
	conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
	cursor = conexion.cursor()

	consulta = 'SELECT id_account, id_tweet, text_tweet, favorite_count_tweet, retweet_count_tweet, eschiste_tweet, ' \
			   'name_account, followers_count_account FROM tweets NATURAL JOIN twitter_accounts'

	cursor.execute(consulta)

	resultado = {}

	for t in cursor.fetchall():
		try:
			print
			#t[2].decode('utf-8')
			#t[6].decode('utf-8')
			tw = Tweet()
			tw.id = t[1]
			tw.texto = t[2]
			tw.favoritos = t[3]
			tw.retweets = t[4]
			tw.es_humor = t[5]
			tw.cuenta = t[6]
			tw.seguidores = t[7]

			resultado[tw.id] = tw
		except UnicodeDecodeError as e:
			print("Error de decode: " + t[2])
			pass

	consulta = 'SELECT id_tweet, nombre_feature, valor_feature FROM features'

	cursor.execute(consulta)

	for t in cursor.fetchall():
		id_tweet = t[0]
		nombre_feature = t[1]
		valor_feature = t[2]
		resultado[id_tweet].features[nombre_feature] = valor_feature

	return list(resultado.values())


def guardar_features(tweets):
	for tweet in tweets:
		tweet.persistir()
