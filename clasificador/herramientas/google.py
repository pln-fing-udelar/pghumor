# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import traceback
import urllib

from lxml import html
import requests


class Google(object):
    @staticmethod
    def esta_en_google(texto):
        try:
            respuesta = requests.get(
                'https://www.google.com.uy/search?' + urllib.urlencode({'q': texto.encode('utf-8')}))
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
