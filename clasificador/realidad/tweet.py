from __future__ import absolute_import
import re

import mysql.connector
from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME

patron_retweet = re.compile('RT @\w+: (.+)', re.UNICODE)


def remover_retweet_si_hay(texto):
	match = re.match(patron_retweet, texto)
	if match is None:
		return texto
	else:
		return match.group(1)


def remover_links(texto):
	return texto


class Tweet:
	def __init__(self):
		self.id = 0
		self.texto = ""
		self.texto_original = ""
		self.retweets = 0
		self.favoritos = 0
		self.cuenta = ""
		self.seguidores = 0
		self.es_humor = False

		self.features = {}

	def persistir(self):
		conexion = mysql.connector.connect(user=DB_USER, password=DB_PASS, host=DB_HOST, database=DB_NAME)
		cursor = conexion.cursor()

		for key, value in self.features.items():
			query = "INSERT INTO features VALUES (" + str(self.id) + ",'" + key + "'," + str(
				value) + ") ON DUPLICATE KEY UPDATE valor_feature = " + str(value)
			cursor.execute(query)

		conexion.commit()

	def preprocesar(self):
		self.texto_original = self.texto
		self.texto = remover_retweet_si_hay(self.texto)
		self.texto = remover_links(self.texto)
