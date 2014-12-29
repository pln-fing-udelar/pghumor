# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import mysql.connector


def cargar_chistes():
    consulta = """
    SELECT
        id_chiste,
        texto_chiste,
        id_clasificacion,
        nombre_clasificacion,
        votacion,
        cantidad_votantes
    FROM chistes
    """
    conexion = mysql.connector.connect(user="root", password="root", host="localhost", database="chistesdotcom")
    cursor = conexion.cursor(buffered=True)  # buffered así sé la cantidad que son antes de iterarlos

    cursor.execute(consulta)

    chistes = []

    for (id_chiste, texto_chiste, id_clasificacion, nombre_clasificacion, votacion, cantidad_votantes) in cursor:
        chiste_nuevo = Chiste(id_chiste, texto_chiste, id_clasificacion, nombre_clasificacion, votacion,
                              cantidad_votantes)
        chistes.append(chiste_nuevo)

    return chistes


def cargar_tweets():
    cargar_evaluacion = False
    conexion = mysql.connector.connect(user="root", password="root", host="localhost", database="corpus")
    cursor = conexion.cursor(buffered=True)  # buffered así sé la cantidad que son antes de iterarlos

    if cargar_evaluacion:
        where_cargar_evaluacion = ''
    else:
        where_cargar_evaluacion = 'WHERE static = 0'

    consulta = """
    SELECT id_account,
           T.id_tweet,
           text_tweet,
           favorite_count_tweet,
           retweet_count_tweet,
           eschiste_tweet,
           name_account,
           followers_count_account,
           static,
           votos,
           votos_no_humor_u_omitido
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
    {where}
    HAVING ( ( votos > 0
               AND votos_no_humor_u_omitido / votos <= 0.25 )
              OR eschiste_tweet = 0 )
    """.format(where=where_cargar_evaluacion)

    cursor.execute(consulta)

    resultado = {}

    for (id_account, tweet_id, texto, favoritos, retweets, es_humor, cuenta, seguidores, evaluacion, votos,
         votos_no_humor_u_omotido) in cursor:
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

        resultado[tw.id] = tw

    return list(resultado.values())


class Chiste:
    def __init__(self, id_chiste, texto_chiste, id_clasificacion, nombre_clasificacion, promedio, votantes):
        self.id_chiste = id_chiste
        self.texto_chiste = texto_chiste
        self.id_clasificacion = id_clasificacion
        self.nombre_clasificacion = nombre_clasificacion
        self.promedio = promedio
        self.votantes = votantes


class Tweet:
    def __init__(self):
        self.cuenta = ""
        self.es_humor = False
        self.evaluacion = False
        self.favoritos = 0
        self.id = 0
        self.retweets = 0
        self.seguidores = 0
        self.texto = ""
        self.texto_original = ""
