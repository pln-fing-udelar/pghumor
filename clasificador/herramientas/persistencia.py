# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from contextlib import closing

import mysql.connector
from progress.bar import IncrementalBar

from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME, SUFIJO_PROGRESS_BAR
from clasificador.realidad.tweet import Tweet


def cargar_tweets(limite=None, agregar_sexuales=False, cargar_features=True):
    """Carga todos los tweets, inclusive aquellos para evaluación, aunque no se quiera evaluar,
    y aquellos mal votados, así se calculan las features para todos. Que el filtro se haga luego."""
    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
    cursor = conexion.cursor(buffered=True)  # buffered así sé la cantidad que son antes de iterarlos

    if limite:
        consulta = "SELECT id_tweet FROM tweets WHERE evaluacion = 0 ORDER BY RAND() LIMIT " + str(limite)

        cursor.execute(consulta)

        bar = IncrementalBar("Eligiendo tweets aleatorios\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
        bar.next(0)

        ids = []

        for (tweet_id,) in cursor:
            ids.append(tweet_id)
            bar.next()

        bar.finish()

        str_ids = '(' + unicode(ids).strip('[]L') + ')'
        consulta_prueba_tweets = "T.id_tweet IN {ids}".format(ids=str_ids)
        consulta_prueba_features = "id_tweet IN {ids}".format(ids=str_ids)

    else:
        consulta_prueba_features = ""
        consulta_prueba_tweets = ""

    if agregar_sexuales:
        consulta_sexuales_tweets = ""
    else:
        consulta_sexuales_tweets = "censurado_tweet = 0"
    consulta_sexuales_features = consulta_sexuales_tweets

    if not agregar_sexuales and limite:
        restricciones_tweets = "WHERE " + consulta_sexuales_tweets + " AND " + consulta_prueba_tweets
        restricciones_features = "WHERE " + consulta_sexuales_features + " AND " + consulta_prueba_features
    elif not agregar_sexuales:
        restricciones_tweets = "WHERE " + consulta_sexuales_tweets
        restricciones_features = "WHERE " + consulta_sexuales_features
    elif limite:
        restricciones_tweets = "WHERE " + consulta_prueba_tweets
        restricciones_features = "WHERE " + consulta_prueba_features
    else:
        restricciones_tweets = ""
        restricciones_features = ""

    consulta = """
    SELECT id_account,
           T.id_tweet,
           text_tweet,
           favorite_count_tweet,
           retweet_count_tweet,
           eschiste_tweet,
           censurado_tweet,
           name_account,
           followers_count_account,
           evaluacion,
           votos,
           votos_humor,
           promedio_votos
    FROM   tweets AS T
           NATURAL JOIN twitter_accounts
                        LEFT JOIN (SELECT id_tweet,
                                          Avg(voto) AS promedio_votos,
                                          Count(*) AS votos,
                                          Count(If(voto <> 'x', 1, NULL)) AS votos_humor
                                   FROM   votos
                                   WHERE voto <> 'n'
                                   GROUP  BY id_tweet) V
                               ON ( V.id_tweet = T.id_tweet )
    {restricciones}
    """.format(restricciones=restricciones_tweets)

    cursor.execute(consulta)

    bar = IncrementalBar("Cargando tweets\t\t\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)

    resultado = {}

    for (id_account, tweet_id, texto, favoritos, retweets, es_humor, censurado, cuenta, seguidores, evaluacion, votos,
         votos_humor, promedio_votos) in cursor:
        tweet = Tweet()
        tweet.id = tweet_id
        tweet.texto_original = texto
        tweet.texto = texto
        tweet.favoritos = favoritos
        tweet.retweets = retweets
        tweet.es_humor = es_humor
        tweet.es_chiste = es_humor
        tweet.censurado = censurado
        tweet.cuenta = cuenta
        tweet.seguidores = seguidores
        tweet.evaluacion = evaluacion
        if votos:
            tweet.votos = int(votos)  # Esta y la siguiente al venir de count y sum, son decimal.
        if votos_humor:
            tweet.votos_humor = int(votos_humor)
        if promedio_votos:
            tweet.promedio_de_humor = promedio_votos

        resultado[tweet.id] = tweet
        bar.next()

    bar.finish()

    if cargar_features:
        consulta = """
        SELECT id_tweet,
               nombre_feature,
               valor_feature
        FROM   features
               NATURAL JOIN tweets
        {restricciones}
        """.format(restricciones=restricciones_features)

        cursor.execute(consulta)

        bar = IncrementalBar("Cargando features\t\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
        bar.next(0)

        for (id_tweet, nombre_feature, valor_feature) in cursor:
            if id_tweet in resultado:
                resultado[id_tweet].features[nombre_feature] = valor_feature
            bar.next()

        bar.finish()

        cursor.close()
        conexion.close()

    return list(resultado.values())


def guardar_features(tweets, **opciones):
    nombre_feature = opciones.pop('nombre_feature', None)
    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
    cursor = conexion.cursor()

    consulta = "INSERT INTO features VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE valor_feature = %s"

    if nombre_feature:
        mensaje = 'Guardando feature ' + nombre_feature
    else:
        mensaje = 'Guardando features'

    bar = IncrementalBar(mensaje, max=len(tweets), suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)

    for tweet in tweets:
        if nombre_feature:
            cursor.execute(
                consulta,
                (
                    tweet.id,
                    nombre_feature,
                    str(tweet.features[nombre_feature]),
                    str(tweet.features[nombre_feature])
                )
            )
        else:
            for key, value in tweet.features.items():
                cursor.execute(consulta, (tweet.id, key, str(value), str(value)))
        bar.next()

    conexion.commit()
    bar.finish()

    cursor.close()
    conexion.close()


def cargar_parecidos_con_distinto_humor():
    with closing(mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)) as conexion:
        # buffered=True así sé la cantidad que son antes de iterarlos.
        with closing(conexion.cursor(buffered=True)) as cursor:
            consulta = """
            SELECT id_tweet_humor,
                   id_tweet_no_humor
            FROM   tweets_parecidos_distinto_humor
            """

            cursor.execute(consulta)

            pares_ids_parecidos_con_distinto_humor = []

            bar = IncrementalBar("Cargando tweets parecidos\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)

            for par_ids in cursor:
                pares_ids_parecidos_con_distinto_humor.append(par_ids)
                bar.next()

            bar.finish()

            return pares_ids_parecidos_con_distinto_humor


def guardar_parecidos_con_distinto_humor(pares_parecidos_distinto_humor):
    with closing(mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)) as conexion:
        with closing(conexion.cursor()) as cursor:
            consulta = "INSERT INTO tweets_parecidos_distinto_humor VALUES (%s, %s)" \
                       + " ON DUPLICATE KEY UPDATE id_tweet_no_humor = %s"

            bar = IncrementalBar("Guardando tweets parecidos\t", max=len(pares_parecidos_distinto_humor),
                                 suffix=SUFIJO_PROGRESS_BAR)
            bar.next(0)

            for tweet_humor, tweet_no_humor in pares_parecidos_distinto_humor:
                cursor.execute(consulta, (tweet_humor.id, tweet_no_humor.id, tweet_no_humor.id))
                bar.next()

            conexion.commit()
            bar.finish()
