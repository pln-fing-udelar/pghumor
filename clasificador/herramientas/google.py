# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from urllib2 import HTTPError
import time
import urllib

from lxml import html
import mechanize
from pkg_resources import resource_filename

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
        browser = mechanize.Browser()
        browser.set_handle_robots(False)
        browser.addheaders = [('User-agent',
                               'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko)'
                               + ' Chrome/39.0.2171.95 Safari/537.36')]

        respuesta_consulta = ""
        salir = False
        while not salir:
            try:
                respuesta_consulta = browser.open("https://www.google.com.uy/search?"
                                                  + urllib.urlencode({'q': palabra.encode('utf-8')}))
                salir = True
            except KeyboardInterrupt:
                raise
            except HTTPError as e:
                print(unicode(e))
                time.sleep(15)
                # respuesta_consulta = requests.get(
                # 'https://www.google.com.uy/search?' + urllib.urlencode({'q': palabra.encode('utf-8')}))
                # salir = respuesta_consulta.status_code == 200
        # assert respuesta_consulta.status_code == 200,
        # "El código de estado de la respuesta_consulta de google debería ser 200"
        texto_html = unicode(respuesta_consulta)
        hay_resultados_consulta = texto_html.find("No se han encontrado resultados") == -1
        arbol_html = html.fromstring(texto_html)
        correccion_gramatical_automatica = arbol_html.xpath('//span[@class="spell"]/text()')
        correccion_gramatical_sugerida = arbol_html.xpath('//span[@class="spell ng"]/text()')
        hay_correccion_gramatical = correccion_gramatical_automatica or correccion_gramatical_sugerida
        return hay_resultados_consulta and not hay_correccion_gramatical
