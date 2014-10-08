from __future__ import absolute_import

import mysql.connector
from progress.bar import Bar

from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME

from clasificador.realidad.tweet import Tweet


def cargar_tweets(**options):
	cargar_evaluacion = options.pop('cargar_evaluacion', False)

	conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
	cursor = conexion.cursor()

	if cargar_evaluacion:
		where_cargar_evaluacion = ''
	else:
		where_cargar_evaluacion = 'WHERE evaluacion = 0'

	consulta = """
	SELECT id_account,
		   T.id_tweet,
		   text_tweet,
		   favorite_count_tweet,
		   retweet_count_tweet,
		   eschiste_tweet,
		   name_account,
		   followers_count_account,
		   evaluacion,
		   votos,
		   votos_no_humor_u_omitido,
		   eschiste_tweet
	FROM   tweets AS T
		   NATURAL JOIN twitter_accounts
						LEFT JOIN (SELECT id_tweet,
										  Count(*) AS votos,
										  Sum(CASE
												WHEN voto = 'x'
													  OR voto = 'n' THEN 1
												ELSE 0
											  end) AS votos_no_humor_u_omitido
								   FROM   votos
								   GROUP  BY id_tweet) V
							   ON ( V.id_tweet = T.id_tweet )
	%s
	HAVING ( ( votos > 0
			   AND votos_no_humor_u_omitido / votos <= 0.25 )
			  OR eschiste_tweet = 0 );
	""" % where_cargar_evaluacion

	cursor.execute(consulta)

	resultado = {}

	for t in cursor.fetchall():
		tw = Tweet()
		tw.id = t[1]
		tw.texto_original = t[2]
		tw.texto = t[2]
		tw.favoritos = t[3]
		tw.retweets = t[4]
		tw.es_humor = t[5]
		tw.cuenta = t[6]
		tw.seguidores = t[7]
		tw.evaluacion = t[8]

		resultado[tw.id] = tw

	consulta = """
	SELECT T.id_tweet,
		   nombre_feature,
		   valor_feature,
		   votos,
		   votos_no_humor_u_omitido,
		   eschiste_tweet
	FROM   features
		   NATURAL JOIN tweets AS T
						LEFT JOIN (SELECT id_tweet,
										  Count(*) AS votos,
										  Sum(CASE
												WHEN voto = 'x'
													  OR voto = 'n' THEN 1
												ELSE 0
											  end) AS votos_no_humor_u_omitido
								   FROM   votos
								   GROUP  BY id_tweet) V
							   ON ( V.id_tweet = T.id_tweet )
	%s
	HAVING ( ( votos > 0
			   AND votos_no_humor_u_omitido / votos <= 0.25 )
			  OR eschiste_tweet = 0 );
    """ % where_cargar_evaluacion

	cursor.execute(consulta)

	for t in cursor.fetchall():
		id_tweet = t[0]
		nombre_feature = t[1]
		valor_feature = t[2]
		resultado[id_tweet].features[nombre_feature] = valor_feature

	return list(resultado.values())


def guardar_features(tweets):
	print "Guardando tweets..."
	bar = Bar('Guardando tweets', max=len(tweets), suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
	bar.next(0)
	for tweet in tweets:
		tweet.persistir()
		bar.next()
	bar.finish()
	print "Fin Guardando tweets"
