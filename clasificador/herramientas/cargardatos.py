from __future__ import absolute_import

import MySQLdb

from clasificador.realidad.tweet import Tweet

DB_HOST = 'localhost'
DB_USER = 'pghumor'
DB_PASS = 'ckP8t/2l'
DB_NAME = 'corpus'


def extraer_tweets():
	datos = [
		DB_HOST,
		DB_USER,
		DB_PASS,
		DB_NAME,
	]

	conexion = MySQLdb.connect(*datos)
	cursor = conexion.cursor()

	consulta = 'SELECT id_account, id_tweet, text_tweet, favorite_count_tweet, retweet_count_tweet, eschiste_tweet, '\
			   'name_account, followers_count_account FROM ' + DB_NAME + '.tweets NATURAL JOIN ' + DB_NAME\
			   + '.twitter_accounts'

	cursor.execute(consulta)

	resultado = []

	for t in cursor.fetchall():
		try:
			t[2].decode('utf-8')
			t[6].decode('utf-8')
			tw = Tweet()
			tw.id = t[1]
			tw.texto = t[2]
			tw.favoritos = t[3]
			tw.retweets = t[4]
			tw.es_humor = t[5]
			tw.cuenta = t[6]
			tw.seguidores = t[7]

			resultado.append(tw)
		except UnicodeDecodeError as e:
			pass

	return resultado
