# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import math
import traceback

from bs4 import BeautifulSoup
import mechanize

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import *
from clasificador.realidad.tweet import *


CARACTERES_ESPANOL = 255

patron_todo_espacios = re.compile(r'^\s*$', re.UNICODE)


def esta_en_diccionario(texto):
    if patron_todo_espacios.match(texto):
        return True

    resultado = Freeling.analyzer_client(texto)

    if len(resultado) == 0:
        return True

    return resultado[0] != (texto + '\n')


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
        # print(search, " se encuentra")
        # else:
        #     print(search, " no se encuentra")

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
            Mide la cantidad de palabras fuera del vocabulario que contiene el texto.
            Tiene en cuenta falta de ortografía, palabras no comunes, cosas como "holaaaaaa", etc.
            Éstas indican menos seriedad en el tweet. Por ejemplo, en una cuenta de CNN no ocurren este
            tipo de cosas. Por lo tanto, no interesa corregir las faltas para detectar la palabra verdadera.
        """

    def calcular_feature(self, tweet):
        texto = tweet.texto
        texto = remover_hashtags(texto)
        texto = remover_usuarios(texto)
        oraciones = Freeling.procesar_texto(texto)
        tokens = list(itertools.chain(*oraciones))
        cant_palabras_oov = 0
        for token in tokens:
            if len(token.token) > 3 and contiene_caracteres_no_espanoles(token.token):
                cant_palabras_oov += 1
            else:
                if not esta_en_diccionario(eliminar_underscore(token.token)):
                    if not google_search(token.token):
                        cant_palabras_oov += 1

        if len(tokens) == 0:
            return 0
        else:
            return cant_palabras_oov / math.sqrt(len(tokens))
