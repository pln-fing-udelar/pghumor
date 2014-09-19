from __future__ import absolute_import
import re

import mysql.connector
from clasificador.herramientas.define import DB_HOST, DB_USER, DB_PASS, DB_NAME

patron_retweet = re.compile(r'RT @\w+: (.+)', re.UNICODE)

patron_url = re.compile(
	r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+',
	re.IGNORECASE)

patron_espacios_multiples = re.compile(r' +')


def remover_retweet_si_hay(texto):
	match = re.match(patron_retweet, texto)
	if match is None:
		return texto
	else:
		return match.group(1)


def remover_links(texto):
	return re.sub(patron_url, '', texto)


def remover_espacios_multiples_y_strip(texto):
	return re.sub(patron_espacios_multiples, ' ', texto).strip()


# TODO: remover usuarios y hashtags
# TODO: html decode
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

		consulta = "INSERT INTO features VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE valor_feature = %s"

		for key, value in self.features.items():
			cursor.execute(consulta, (self.id, key, value, value))

		conexion.commit()

	def preprocesar(self):
		self.texto_original = self.texto
		self.texto = remover_retweet_si_hay(self.texto)
		self.texto = remover_links(self.texto)
		self.texto = remover_espacios_multiples_y_strip(self.texto)
