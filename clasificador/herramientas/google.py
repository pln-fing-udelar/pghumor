# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import traceback
import urllib

from lxml import html
from pkg_resources import resource_filename
import requests

import clasificador.herramientas.utils


class Google(object):
    diccionario_positivo = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'DiccionarioGoogle.txt'))
    diccionario_negativo = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'DiccionarioNoGoogle.txt'))

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
                with open(resource_filename('clasificador.recursos.diccionarios', 'DiccionarioGoogle.txt'),
                          'a') as archivo:
                    archivo.write((palabra + '\n').encode('utf-8'))
            else:
                Google.diccionario_negativo.add(palabra)
                with open(resource_filename('clasificador.recursos.diccionarios', 'DiccionarioNoGoogle.txt'),
                          'a') as archivo:
                    archivo.write((palabra + '\n').encode('utf-8'))
            return esta_en_google_palabra

    @staticmethod
    def esta_en_google_consulta(palabra):
        try:
            respuesta = requests.get(
                'https://www.google.com.uy/search?' + urllib.urlencode({'q': palabra.encode('utf-8')}))
            assert respuesta.status_code == 200, "El código de estado de la respuesta de google debería ser 200"
            arbol_html = html.fromstring(respuesta.text)
            correccion_gramatical_automatica = arbol_html.xpath('//span[@class="spell"]/text()')
            correccion_gramatical_sugerida = arbol_html.xpath('//span[@class="spell ng"]/text()')
            hay_resultados = respuesta.text.find("No se han encontrado resultados") == -1
            return hay_resultados and not correccion_gramatical_automatica and not correccion_gramatical_sugerida
        except KeyboardInterrupt:
            raise
        except Exception:
            traceback.print_exc()
            return False
