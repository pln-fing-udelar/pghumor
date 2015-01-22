# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import time
import urllib

from lxml import html
from pkg_resources import resource_filename
import requests

import clasificador.herramientas.utils


class Google(object):
    diccionario_positivo = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'google.dic'))
    diccionario_negativo = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'nogoogle.dic'))

    @staticmethod
    def esta_en_google(palabra):
        if palabra in Google.diccionario_positivo:
            return True
        elif palabra in Google.diccionario_negativo:
            return False
        else:
            esta_en_google_palabra = Google.esta_en_google_consulta(palabra)
            if esta_en_google_palabra:
                Google.diccionario_positivo.add(palabra)
                with open(resource_filename('clasificador.recursos.diccionarios', 'google.dic'),
                          'a') as archivo:
                    archivo.write((palabra + '\n').encode('utf-8'))
            else:
                Google.diccionario_negativo.add(palabra)
                with open(resource_filename('clasificador.recursos.diccionarios', 'nogoogle.dic'),
                          'a') as archivo:
                    archivo.write((palabra + '\n').encode('utf-8'))
            return esta_en_google_palabra

    @staticmethod
    def esta_en_google_consulta(palabra):
        respuesta = ""
        while True:
            respuesta = requests.get('https://www.google.com.uy/search?'
                                     + urllib.urlencode({'q': palabra.encode('utf-8')}))
            time.sleep(2.5)
            if respuesta.status_code == 200:
                break
            else:
                print(respuesta.status_code)

        hay_resultados = respuesta.text.find("No se han encontrado resultados") == -1
        arbol_html = html.fromstring(respuesta.text)
        correccion_gramatical_automatica = arbol_html.xpath('//span[@class="spell"]/text()')
        correccion_gramatical_sugerida = arbol_html.xpath('//span[@class="spell ng"]/text()')
        hay_correccion_gramatical = bool(correccion_gramatical_automatica) or bool(correccion_gramatical_sugerida)
        return hay_resultados and not hay_correccion_gramatical
