# coding=utf-8
from __future__ import absolute_import, unicode_literals

import mysql.connector
from progress.bar import Bar

from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME, DB_NAME_CHISTES_DOT_COM
from clasificador.realidad.tweet import Tweet
from clasificador.realidad.chiste import Chiste


def cargar_tweets(prueba=False):
    """Carga todos los tweets, inclusive aquellos para evaluación, aunque no se quiera evaluar,
    y aquellos mal votados, así se calculan las features para todos. Que el filtro se haga luego.

    """
    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
    cursor = conexion.cursor(buffered=True)  # buffered así sé la cantidad que son antes de iterarlos

    if prueba:
        consulta = "SELECT id_tweet FROM tweets WHERE evaluacion = 0 ORDER BY RAND() LIMIT 1000"
        cursor.execute(consulta)

        bar = Bar('Cargando tweets de prueba', max=cursor.rowcount,
                  suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
        bar.next(0)

        ids = []

        for (tweet_id,) in cursor:
            ids.append(tweet_id)
            bar.next()

        bar.finish()

        str_ids = "(" + str(ids).strip("[]") + ")"

        consulta_prueba_tweets = "WHERE T.id_tweet IN {ids}".format(ids=str_ids)
        consulta_prueba_features = "WHERE id_tweet IN {ids}".format(ids=str_ids)
    else:
        consulta_prueba_tweets = ""
        consulta_prueba_features = ""

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
    {filtro_prueba}
    """.format(filtro_prueba=consulta_prueba_tweets)

    cursor.execute(consulta)

    bar = Bar('Cargando tweets', max=cursor.rowcount, suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
    bar.next(0)

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

        resultado[tw.id] = tw
        bar.next()

    bar.finish()

    consulta = """
    SELECT id_tweet,
           nombre_feature,
           valor_feature
    FROM   features
    {filtro_prueba}
    """.format(filtro_prueba=consulta_prueba_features)

    cursor.execute(consulta)

    bar = Bar('Cargando features', max=cursor.rowcount, suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
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

    bar = Bar(mensaje, max=len(tweets), suffix='%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds')
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
    conexion.disconnect()

# ##############################################################
# ####   PRIMITIVAS PACA ACCEDER A CHISTES DE CHISTE.COM   #####
# ##############################################################


def cargar_chistes_pagina():
    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME_CHISTES_DOT_COM)
    cursor = conexion.cursor(buffered=True)  # buffered así sé la cantidad que son antes de iterarlos

    consulta = """
        SELECT id_chiste,
               texto_chiste,
               id_clasificacion,
               nombre_clasificacion,
               votacion,
               cantidad_votantes
        FROM   chistes
        """

    cursor.execute(consulta)

    chistes = []
    for (id_chiste, texto_chiste, id_clasificacion, nombre_clasificacion, votacion, cantidad_votantes) in cursor:
        chiste = Chiste()
        chiste.id_chiste = id_chiste
        chiste.texto_chiste = texto_chiste
        chiste.id_clasificacion = id_clasificacion
        chiste.nombre_clasificacion = nombre_clasificacion
        chiste.votacion = votacion
        chiste.cantidad_votantes = cantidad_votantes
        chistes.append(chiste)

    return chistes


def obtener_chistes_categoria(categoria):

    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME_CHISTES_DOT_COM)
    cursor = conexion.cursor(buffered=True)  # buffered así sé la cantidad que son antes de iterarlos

    consulta = """
        SELECT id_chiste,
               texto_chiste,
               id_clasificacion,
               nombre_clasificacion,
               votacion,
               cantidad_votantes
        FROM   chistes
        WHERE id_clasificacion =
        """

    consulta += str(categoria)

    cursor.execute(consulta)

    chistes = []
    for (id_chiste, texto_chiste, id_clasificacion, nombre_clasificacion, votacion, cantidad_votantes) in cursor:
        chiste = Chiste()
        chiste.id_chiste = id_chiste
        chiste.texto_chiste = texto_chiste
        chiste.id_clasificacion = id_clasificacion
        chiste.nombre_clasificacion = nombre_clasificacion
        chiste.votacion = votacion
        chiste.cantidad_votantes = cantidad_votantes
        chistes.append(chiste)

    return chistes


def obtener_categorias():

    conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME_CHISTES_DOT_COM)
    cursor = conexion.cursor()

    consulta = """
            SELECT DISTINCT id_clasificacion, nombre_clasificacion
            FROM chistesdotcom.chistes;
        """

    cursor.execute(consulta)

    categorias = []
    for (id_clasificacion, nombre_clasificacion) in cursor:
        categoria = {'id_clasificacion': id_clasificacion, 'nombre_clasificacion': nombre_clasificacion}
        categorias.append(categoria)

    return categorias