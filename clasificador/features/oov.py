# -*- coding: utf-8 -*-
from __future__ import absolute_import
import traceback
import math
import re

from bs4 import BeautifulSoup
import mechanize

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import *
from clasificador.herramientas.utils import *
from clasificador.realidad.tweet import *

CARACTERES_ESPANOL = 255


def esta_en_diccionario(texto):
    if re.search('^\s*$', texto) is not None:
        return True

    command = 'echo "' + texto + '" | analyzer_client 11111'
    resultado = ejecutar_comando(command)
    while (len(resultado) == 0) or (
            (len(resultado) > 0) and resultado[0] == '/bin/sh: fork: Resource temporarily unavailable\n' or resultado[
        0] == 'Server not ready?\n'):
        print resultado
        print len(texto), texto
        print "En este loop"
        resultado = ejecutar_comando(command)

    if len(resultado) == 0:
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
        browser.addheaders = [('User-agent', 'Mozilla')]

        htmltext = browser.open("https://www.google.com.uy/search?q=" + search)
        # img_urls = []
        soup = BeautifulSoup(htmltext)
        result = soup.findAll("body")
        se_encuentra = '<div id="_FQd" ' not in str(result[0])
        # if se_encuentra:
        # print search, " se encuentra"
        # else:
        #	print search, " no se encuentra"

        return se_encuentra
    except Exception:
        traceback.print_exc()
        return False


def eliminar_underscore(token):
    return token.replace('_', ' ')


class OOV(Feature):
    def __init__(self):
        super(OOV, self).__init__()
        self.nombre = "OOV"
        self.descripcion = """
			Esta característica mide la cantidad de palabras fuera del vocabulario que contiene el texto.
			Tiene en cuenta falta de ortografía, palabras no comunes, cosas como "holaaaaaa", etc.
			Éstas indican menos seriedad en el tweet. Por ejemplo, en una cuenta de CNN no ocurren este
			tipo de cosas. Por lo tanto, no interesa corregir las faltas para detectar la palabra verdadera.
		"""

    def calcular_feature(self, tweet):
        texto = tweet.texto
        texto = remover_hashtags(texto)
        texto = remover_usuarios(texto)
        tokens = Freeling.procesar_texto(texto)
        cant_palabras_oov = 0
        for token in tokens:

            if len(token.token) > 3 and contiene_caracteres_no_espanoles(token.token):
                cant_palabras_oov += 1
            else:
                if not esta_en_diccionario(eliminar_underscore(token.token)):
                    if not google_search(token.token):
                        cant_palabras_oov += 1

        if len(tokens) == 0:
            tweet.features[self.nombre] = 0
        else:
            tweet.features[self.nombre] = cant_palabras_oov / math.sqrt(len(tokens))
