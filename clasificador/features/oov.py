# -*- coding: utf-8 -*-
from __future__ import absolute_import

CARACTERES_ESPANOL = 255

from pkg_resources import resource_filename
import math

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import *
from clasificador.herramientas.treetagger import *
from clasificador.herramientas.utils import *
from clasificador.realidad.tweet import *

from bs4 import BeautifulSoup
import mechanize


def esta_en_diccionario(texto):
	resultado = ejecutar_comando("echo '" + texto + "' | analyzer_client 11111")
	if len(resultado) == 0:
		print "No hay resultado para la plabra: ", texto, "de largo: ", len(texto)
		return True
	return resultado[0] != (texto + "\n")


def contiene_caracteres_no_espanoles(texto):
	for c in texto:
		if ord(c) > CARACTERES_ESPANOL:
			return True

	return False


def google_search(search):
	try:
		browser = mechanize.Browser()
		browser.set_handle_robots(False)
		browser.addheaders = [('User-agent','Mozilla')]

		htmltext = browser.open("https://www.google.com.uy/search?q=" + search)
		img_urls = []
		soup = BeautifulSoup(htmltext)
		result = soup.findAll("body")
		se_encuentra = '<div id="_FQd" ' not in str(result[0])
		#if se_encuentra:
		#	print search, " se encuentra"
		#else:
		#	print search, " no se encuentra"

		return se_encuentra
	except Exception:
		print "error"
		return False

def eliminar_underscore(token):
		return token.replace('_', ' ')

class OOV(Feature):

	def __init__(self):
		super(OOV, self).__init__()
		self.nombre = "OOV"
		self.diccionario = obtener_diccionario(resource_filename('clasificador.recursos.diccionarios', 'lemario-espanol.txt'))

	def calcular_feature(self, tweet):
		texto = tweet.texto
		texto = remover_hashtags(texto)
		texto = remover_usuarios(texto)
		tokens = Freeling.procesar_texto(texto)
		cant_palabras_oov = 0
		for token in tokens:

			if len(token.token) > 3 and contiene_caracteres_no_espanoles(token.token):
				cant_palabras_oov += 1
				print token.token, " - ", tweet.es_humor, " - ", tweet.texto_original, "\n"
			else:
				if not esta_en_diccionario(eliminar_underscore(token.token)):
					if not google_search(token.token):
						cant_palabras_oov += 1
						print token.token, " - ", tweet.es_humor, " - ", tweet.texto_original, "\n"

		if len(tokens) == 0:
			print("Error: ", tweet.texto)
			tweet.features[self.nombre] = 0
		else:
			tweet.features[self.nombre] = cant_palabras_oov/math.sqrt(len(tokens))
