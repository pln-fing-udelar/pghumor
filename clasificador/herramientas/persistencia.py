# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import mysql.connector

from progress.bar import Bar

from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME, SUFIJO_PROGRESS_BAR
from clasificador.realidad.tweet import Tweet


def cargar_tweets(limite=None, cargar_features=True, rank=0):
    """Carga todos los tweets, inclusive aquellos para evaluación, aunque no se quiera evaluar,
    y aquellos mal votados, así se calculan las features para todos. Que el filtro se haga luego."""
    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
    cursor = conexion.cursor(buffered=True)  # buffered así sé la cantidad que son antes de iterarlos

    consulta = "SELECT count(*) as cantidad FROM tweets "
    cursor.execute(consulta)

    bar = Bar("Eligiendo tweets aleatorios\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)

    # ids = []

    for (cantidad,) in cursor:
        cant_tweets_total = int(cantidad)
        bar.next()

    bar.finish()

    if limite:
        #consulta = "SELECT id_tweet FROM tweets WHERE evaluacion = 0 ORDER BY RAND() LIMIT " + str(limite)

        #cursor.execute(consulta)

        #bar = Bar("Eligiendo tweets aleatorios\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
        #bar.next(0)

        #ids = []

        #for (tweet_id,) in cursor:
         #   ids.append(tweet_id)
          #  bar.next()

        #bar.finish()

        #str_ids = "(" + unicode(ids).strip("[]L") + ")"

        #consulta_prueba_tweets = "WHERE T.id_tweet IN {ids}".format(ids=str_ids)
        #consulta_prueba_features = "WHERE id_tweet IN {ids}".format(ids=str_ids)

       # consulta = "SELECT count(*) as cantidad FROM tweets "
       # cursor.execute(consulta)

        #bar = Bar("Eligiendo tweets aleatorios\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
        #bar.next(0)

        #ids = []

        cant_tweets = int(cant_tweets_total / limite)

        # cant_tweets = 200  # para probar con pocos
        #       str_ids = "(" + unicode(ids).strip("[]L") + ")"

        consulta_prueba_tweets = ""
        consulta_prueba_features = ""
    else:
        consulta_prueba_tweets = ""
        consulta_prueba_features = ""
        cant_tweets = cant_tweets_total
        # cant_tweets = 400  # para probar con pocos

    indice = rank * cant_tweets

    print(str("Indice: " + str(indice) + " cantTweets: " + str(cant_tweets)))

    consulta = """
    SELECT  id_account,
           T.id_tweet,
           text_tweet,
           favorite_count_tweet,
           retweet_count_tweet,
           eschiste_tweet,
           name_account,
           followers_count_account,
           evaluacion,
           votos,
           votos_humor
    FROM   tweets AS T
           NATURAL JOIN twitter_accounts
                        LEFT JOIN (SELECT id_tweet,
                                          Count(*) AS votos,
                                          Count(If(voto <> 'x', 1, NULL)) AS votos_humor
                                   FROM   votos
                                   WHERE voto <> 'n'
                                   GROUP  BY id_tweet) V
                               ON ( V.id_tweet = T.id_tweet )
    ORDER BY T.id_tweet
    LIMIT """ + str(indice) + """,""" + str(cant_tweets) + """
    """.format(filtro_prueba=consulta_prueba_tweets)

    cursor.execute(consulta)
    print("Pre cargados tweets - agregado")
    bar = Bar("Cargando tweets\t\t\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)
    ids=[]
    resultado = {}

    for (id_account, tweet_id, texto, favoritos, retweets, es_humor, cuenta, seguidores, evaluacion, votos,
         votos_humor) in cursor:
        tw = Tweet()
        tw.id = tweet_id
        tw.texto_original = texto
        tw.texto = texto
        tw.favoritos = favoritos
        tw.retweets = retweets
        tw.es_humor = es_humor
        tw.cuenta = cuenta
        tw.seguidores = seguidores
        tw.evaluacion = evaluacion
        if votos:
            tw.votos = int(votos)  # Esta y la siguiente al venir de count y sum, son decimal.
        if votos_humor:
            tw.votos_humor = int(votos_humor)
        ids.append(tweet_id)
        resultado[tw.id] = tw
        bar.next()
    print("Pre cargado arreglo de tweets")
    bar.finish()
    str_ids = "(" + unicode(ids).strip("[]") + ")"
    str_ids = str_ids.replace("L", "")
    # consulta_prueba_features = "WHERE id_tweet IN {ids}".format(ids=str_ids)
    consulta_prueba_features = ""

    if cargar_features:
        consulta = """
        SELECT features.id_tweet,
               nombre_feature,
               valor_feature
        FROM   features
            INNER JOIN (SELECT id_tweet FROM tweets ORDER BY id_tweet
                LIMIT """ + str(indice) + """,""" + str(cant_tweets) + """) AS T ON features.id_tweet=T.id_tweet
        {filtro_prueba}
        """.format(filtro_prueba=consulta_prueba_features)

        cursor.execute(consulta)
        print("Pre cargados features - agregado 2")
        bar = Bar("Cargando features\t\t", max=cursor.rowcount, suffix=SUFIJO_PROGRESS_BAR)
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

    bar = Bar(mensaje, max=len(tweets), suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)

    for tweet in tweets:
        if nombre_feature:
            cursor.execute(consulta,
                           (tweet.id, nombre_feature, str(tweet.features[nombre_feature]),
                            str(tweet.features[nombre_feature])))
        else:
            for key, value in tweet.features.items():
                cursor.execute(consulta, (tweet.id, key, str(value), str(value)))
        bar.next()

    conexion.commit()
    bar.finish()

    cursor.close()
    conexion.close()

def guardar_feature(tweet, nombre_feature, valor_feature):
    #nombre_feature = opciones.pop('nombre_feature', None)
    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
    cursor = conexion.cursor()

    consulta = "INSERT INTO features VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE valor_feature = %s"

    cursor.execute(consulta,
                           (tweet.id, nombre_feature, str(valor_feature),  str(valor_feature)))
    conexion.commit()
    cursor.close()
    conexion.close()
    #i=1