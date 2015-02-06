# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

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
        if agregar_sexuales:
            consulta = "SELECT id_tweet FROM tweets WHERE evaluacion = 0 ORDER BY RAND() LIMIT " + str(limite)
        else:
            consulta = "SELECT id_tweet FROM tweets WHERE evaluacion = 0 AND censurado_tweet = 0 ORDER BY RAND() LIMIT "\
                       + str(limite)

        cursor.execute(consulta)

        bar = IncrementalBar("Eligiendo tweets aleatorios\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
        bar.next(0)

        ids = []

        for (tweet_id,) in cursor:
            ids.append(tweet_id)
            bar.next()

        bar.finish()

        str_ids = "(" + unicode(ids).strip("[]L") + ")"
        consulta_prueba_tweets = "WHERE T.id_tweet IN {ids}".format(ids=str_ids)
        consulta_prueba_features = "WHERE id_tweet IN {ids}".format(ids=str_ids)

    else:
        consulta_prueba_tweets = ""
        if not agregar_sexuales:
            consulta_prueba_tweets = "WHERE censurado_tweet = 0"
        consulta_prueba_features = ""

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
    {filtro_prueba}
    """.format(filtro_prueba=consulta_prueba_tweets)

    cursor.execute(consulta)

    bar = IncrementalBar("Cargando tweets\t\t\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)

    resultado = {}

    for (id_account, tweet_id, texto, favoritos, retweets, es_humor, censurado, cuenta, seguidores, evaluacion, votos,
         votos_humor, promedio_votos) in cursor:
        tw = Tweet()
        tw.id = tweet_id
        tw.texto_original = texto
        tw.texto = texto
        tw.favoritos = favoritos
        tw.retweets = retweets
        tw.es_humor = es_humor
        tw.censurado = censurado
        tw.cuenta = cuenta
        tw.seguidores = seguidores
        tw.evaluacion = evaluacion
        if votos:
            tw.votos = int(votos)  # Esta y la siguiente al venir de count y sum, son decimal.
        if votos_humor:
            tw.votos_humor = int(votos_humor)
        if promedio_votos:
            tw.promedio_de_humor = promedio_votos

        resultado[tw.id] = tw
        bar.next()

    bar.finish()

    if cargar_features:
        consulta = """
        SELECT id_tweet,
               nombre_feature,
               valor_feature
        FROM   features
        {filtro_prueba}
        """.format(filtro_prueba=consulta_prueba_features)

        cursor.execute(consulta)

        bar = IncrementalBar("Cargando features\t\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
        bar.next(0)

        for (id_tweet, nombre_feature, valor_feature) in cursor:
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
