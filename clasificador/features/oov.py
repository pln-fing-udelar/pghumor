# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import itertools
import math
import traceback
import urllib

from lxml import html
import requests

from clasificador.features.feature import Feature
from clasificador.herramientas.freeling import Freeling
from clasificador.realidad.tweet import *


CARACTERES_ESPANOL = 255

patron_todo_espacios = re.compile(r'^\s*$', re.UNICODE)


def contiene_caracteres_no_espanoles(texto):
    return any(ord(c) > CARACTERES_ESPANOL for c in texto)


def esta_en_google(texto):
    try:
        respuesta = requests.get('https://www.google.com.uy/search?' + urllib.urlencode({'q': texto.encode('utf-8')}))
        assert respuesta.status_code == 200, "El código de estado de la respuesta de google debería ser 200"
        arbol_html = html.fromstring(respuesta.text)
        correccion_gramatical_automatica = arbol_html.xpath('//span[@class="spell"]/text()')
        correccion_gramatical_sugerida = arbol_html.xpath('//span[@class="spell ng"]/text()')
        # TODO: falta fijarse si hay resultados en la consulta a google
        return not correccion_gramatical_automatica and not correccion_gramatical_sugerida
    except KeyboardInterrupt:
        raise
    except Exception:
        traceback.print_exc()
        return False


def eliminar_underscores(texto):
    return texto.replace('_', ' ')


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
        for token_freeling in tokens:
            token = eliminar_underscores(token_freeling.token)
            if (len(token) > 3 and contiene_caracteres_no_espanoles(token)) \
                    or (not Freeling.esta_en_diccionario(token) and not esta_en_google(token)):
                cant_palabras_oov += 1

        if len(tokens) == 0:
            return 0
        else:
            return cant_palabras_oov / math.sqrt(len(tokens))
