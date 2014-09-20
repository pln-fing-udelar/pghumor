from __future__ import absolute_import
import re

import mysql.connector
from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME

import HTMLParser # import html.parser # in python 3

patron_retweet = re.compile(r'^RT @\w+: ', re.UNICODE)

patron_url = re.compile(
	r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
	re.IGNORECASE)

patron_espacios_multiples = re.compile(r' +')

patron_hashtag = re.compile(r'\B#\w+')

patron_usuario = re.compile(r'\B@\w+')


def remover_retweet_si_hay(texto):
	return re.sub(patron_retweet, '', texto)


def remover_links(texto):
	return re.sub(patron_url, '', texto)


def remover_hashtags(texto):
	return re.sub(patron_hashtag, '', texto)


def remover_usuarios(texto):
	return re.sub(patron_usuario, '', texto)


def remover_espacios_multiples_y_strip(texto):
	return re.sub(patron_espacios_multiples, ' ', texto).strip()


class Tweet:
	def __init__(self):
		self.cuenta = ""
		self.es_humor = False
		self.favoritos = 0
		self.id = 0
		self.retweets = 0
		self.seguidores = 0
		self.texto = ""
		self.texto_original = ""

		self.features = {}

	def persistir(self):
		conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
		cursor = conexion.cursor()

		consulta = "INSERT INTO features VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE valor_feature = %s"

		for key, value in self.features.items():
			cursor.execute(consulta, (self.id, key, value, value))

		conexion.commit()

	def preprocesar(self):
		self.texto_original = self.texto
		self.texto = HTMLParser.HTMLParser().unescape(self.texto)
		self.texto = remover_retweet_si_hay(self.texto)
		self.texto = remover_links(self.texto)
		self.texto = remover_espacios_multiples_y_strip(self.texto)
