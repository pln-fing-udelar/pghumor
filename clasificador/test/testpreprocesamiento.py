# coding=utf-8
from __future__ import absolute_import, unicode_literals

import unittest

from clasificador.realidad.tweet import Tweet, remover_retweet_si_hay, remover_links, \
    remover_espacios_multiples_y_strip, \
    remover_hashtags, remover_usuarios


class TestPreprocesamiento(unittest.TestCase):
    def test_remover_retweet_basico(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = 'RT @GustavoMazy: @LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!'
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        self.assertEqual(remover_retweet_si_hay(tweet.texto),
                         '@LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!',
                         "El texto sin el retweet no es el esperado")

    def test_remover_retweet_con_usuario_con_acentos(self):
        tweet = Tweet()
        tweet.id = 58179039764021248
        tweet.texto = 'RT @GuñavoMázy: @LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!'
        tweet.favoritos = 3
        tweet.retweets = 14
        tweet.es_humor = 1
        tweet.cuenta = 132679073

        self.assertEqual(remover_retweet_si_hay(tweet.texto),
                         '@LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!',
                         "El texto sin el retweet no es el esperado")

    def test_remover_links_basico(self):
        tweet = Tweet()
        tweet.id = 19821138922184705
        tweet.texto = 'FOTO CURIOSA: ¿Será culpa del arquitecto? ¿Tu que opinas? http://losgraficos.com/fotos-imagenes-graciosas-1381.html #fb'
        tweet.favoritos = 5
        tweet.retweets = 26
        tweet.es_humor = 1
        tweet.cuenta = 174450359

        self.assertEqual(remover_links(tweet.texto),
                         u'FOTO CURIOSA: ¿Será culpa del arquitecto? ¿Tu que opinas?  #fb',
                         "El texto sin el link no es el esperado")

    def test_remover_dos_links(self):
        tweet = Tweet()
        tweet.id = 301726981937057792
        tweet.texto = 'RT @laseptimabutaca: Trailer de "Rápido y Furioso 6" que se estrenará en mayo de este año 2013 http://t.co/tklxfuFx http://t.co/c5aS4hw2'
        tweet.favoritos = 0
        tweet.retweets = 71
        tweet.es_humor = 1
        tweet.cuenta = 142482558

        self.assertEqual(remover_links(tweet.texto),
                         'RT @laseptimabutaca: Trailer de "Rápido y Furioso 6" que se estrenará en mayo de este año 2013  ',
                         "El texto sin los links no es el esperado")

    def test_remover_espacios_multiples_y_strip(self):
        tweet = Tweet()
        tweet.id = 301726981937057792
        tweet.texto = 'RT    @laseptimabutaca: Trailer de "Rápido y Furioso 6"  que     se estrenará en mayo de este año 2013  '
        tweet.favoritos = 0
        tweet.retweets = 71
        tweet.es_humor = 1
        tweet.cuenta = 142482558

        self.assertEqual(remover_espacios_multiples_y_strip(tweet.texto),
                         'RT @laseptimabutaca: Trailer de "Rápido y Furioso 6" que se estrenará en mayo de este año 2013',
                         "El texto sin los espacios múltiples y sin strip no es el esperado")

    def test_remover_hashtags(self):
        tweet = Tweet()
        tweet.id = 301726981937057792
        tweet.texto = '#DiaMundialDelOrgasmoFemenino Lol Respeten un poco Este TT es igual como si fuese #ILoveReggaeton Que gracia  siempre #CojenComoObjetoSexual'
        tweet.favoritos = 0
        tweet.retweets = 71
        tweet.es_humor = 1
        tweet.cuenta = 142482558

        self.assertEqual(remover_hashtags(tweet.texto),
                         ' Lol Respeten un poco Este TT es igual como si fuese  Que gracia  siempre ',
                         "El texto sin los hashtags no es el esperado")

    def test_remover_hashtags_con_acento(self):
        tweet = Tweet()
        tweet.id = 301726981937057792
        tweet.texto = '#DíaMundialDelOrgasmoFemenino Lol Respeten un poco Este TT es igual como si fuese #ILoveReggaeton Que gracia  siempre #CojenComoObjetoSexual'
        tweet.favoritos = 0
        tweet.retweets = 71
        tweet.es_humor = 1
        tweet.cuenta = 142482558

        self.assertEqual(remover_hashtags(tweet.texto),
                         ' Lol Respeten un poco Este TT es igual como si fuese  Que gracia  siempre ',
                         "El texto sin los hashtags no es el esperado")

    def test_remover_usuarios(self):
        tweet = Tweet()
        tweet.id = 301726981937057792
        tweet.texto = '#ThankYou @clauditaa_love @vivirocha17 @jeanm23 @freddycastro19 @eleze12 @josfersp @vicenteanthonio Retuiters destacados de hoy, gracias!'
        tweet.favoritos = 0
        tweet.retweets = 71
        tweet.es_humor = 1
        tweet.cuenta = 142482558

        self.assertEqual(remover_usuarios(tweet.texto),
                         '#ThankYou        Retuiters destacados de hoy, gracias!',
                         "El texto sin los usuarios no es el esperado")

    def test_remover_usuarios_con_acento(self):
        tweet = Tweet()
        tweet.id = 301726981937057792
        tweet.texto = '#ThankYou @clauditaa_love @vivirocha17 @jeanm23 @freddycastro19 @eleze12 @josférsp @vicenteanthonio Retuiters destacados de hoy, gracias!'
        tweet.favoritos = 0
        tweet.retweets = 71
        tweet.es_humor = 1
        tweet.cuenta = 142482558

        self.assertEqual(remover_usuarios(tweet.texto),
                         '#ThankYou        Retuiters destacados de hoy, gracias!',
                         "El texto sin los usuarios no es el esperado")


if __name__ == '__main__':
    unittest.main()
