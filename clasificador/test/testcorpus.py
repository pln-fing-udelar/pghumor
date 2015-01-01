# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from contextlib import closing
import unittest

import mysql.connector

from clasificador.herramientas.define import DB_HOST, DB_NAME, DB_PASS, DB_USER


class TestCorpus(unittest.TestCase):
    def test_tweets_humor_con_votos_repetido(self):
        with closing(mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST,
                                             database=DB_NAME)) as conexion, closing(conexion.cursor()) as cursor:
            consulta = """
                SELECT Count(*)
                FROM (SELECT Count(*) AS cuenta
                      FROM   (SELECT text_tweet,
                                     eschiste_tweet
                              FROM   tweets
                                     NATURAL JOIN votos
                              GROUP  BY id_tweet) S
                      WHERE eschiste_tweet = 1
                      GROUP  BY text_tweet
                      HAVING cuenta > 1
                      ORDER  BY cuenta desc) T
                """
            cursor.execute(consulta)
            resultados = cursor.fetchone()[0]
            self.assertEquals(0, resultados,
                              "No debería haber tweets de humor duplicados con votos, pero se encontraron "
                              + str(resultados))


if __name__ == '__main__':
    unittest.main()
