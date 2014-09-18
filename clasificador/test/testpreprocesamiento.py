# coding=utf-8
import unittest
from clasificador.realidad.tweet import Tweet, remover_retweet_si_hay, remover_links, remover_espacios_multiples_y_strip


class TestSequenceFunctions(unittest.TestCase):
	def test_remover_retweet_basico(self):
		tweet = Tweet()
		tweet.id = 58179039764021248
		tweet.texto = u'RT @GustavoMazy: @LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!'
		tweet.favoritos = 3
		tweet.retweets = 14
		tweet.es_humor = 1
		tweet.cuenta = 132679073

		self.assertEqual(remover_retweet_si_hay(tweet.texto),
						 u'@LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!',
						 "El texto sin el retweet no es el esperado")

	def test_remover_retweet_con_usuario_con_acentos(self):
		tweet = Tweet()
		tweet.id = 58179039764021248
		tweet.texto = u'RT @GuñavoMázy: @LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!'
		tweet.favoritos = 3
		tweet.retweets = 14
		tweet.es_humor = 1
		tweet.cuenta = 132679073

		self.assertEqual(remover_retweet_si_hay(tweet.texto),
						 u'@LosChistes feliz aniversario de un año en twitter! //Cierto, estamos cumpliendo UN AÑO, GRACIAS a todos!',
						 "El texto sin el retweet no es el esperado")

	def test_remover_links_basico(self):
		tweet = Tweet()
		tweet.id = 19821138922184705
		tweet.texto = u'FOTO CURIOSA: ¿Será culpa del arquitecto? ¿Tu que opinas? http://losgraficos.com/fotos-imagenes-graciosas-1381.html #fb'
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
		tweet.texto = u'RT @laseptimabutaca: Trailer de "Rápido y Furioso 6" que se estrenará en mayo de este año 2013 http://t.co/tklxfuFx http://t.co/c5aS4hw2'
		tweet.favoritos = 0
		tweet.retweets = 71
		tweet.es_humor = 1
		tweet.cuenta = 142482558

		self.assertEqual(remover_links(tweet.texto),
						 u'RT @laseptimabutaca: Trailer de "Rápido y Furioso 6" que se estrenará en mayo de este año 2013  ',
						 "El texto sin los links no es el esperado")

	def test_remover_espacios_multiples_y_strip(self):
		tweet = Tweet()
		tweet.id = 301726981937057792
		tweet.texto = u'RT    @laseptimabutaca: Trailer de "Rápido y Furioso 6"  que     se estrenará en mayo de este año 2013  '
		tweet.favoritos = 0
		tweet.retweets = 71
		tweet.es_humor = 1
		tweet.cuenta = 142482558

		self.assertEqual(remover_espacios_multiples_y_strip(tweet.texto),
						 u'RT @laseptimabutaca: Trailer de "Rápido y Furioso 6" que se estrenará en mayo de este año 2013',
						 u"El texto sin los espacios múltiples y sin strip no es el esperado")


if __name__ == '__main__':
	unittest.main()
