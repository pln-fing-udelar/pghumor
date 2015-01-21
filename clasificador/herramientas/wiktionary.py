# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import json
import urllib

from pkg_resources import resource_filename
import requests

import clasificador.herramientas.utils


class Wiktionary(object):
    diccionario_positivo = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'Wikctionary.dic'))
    diccionario_negativo = clasificador.herramientas.utils.obtener_diccionario(
        resource_filename('clasificador.recursos.diccionarios', 'NoWikctionary.dic'))

    @staticmethod
    def pertenece(palabra):
        if palabra in Wiktionary.diccionario_positivo:
            return True
        elif palabra in Wiktionary.diccionario_negativo:
            return False
        else:
            pertenece_palabra = Wiktionary.pertenece_consulta(palabra)
            if pertenece_palabra:
                Wiktionary.diccionario_positivo.add(palabra)
                with open(resource_filename('clasificador.recursos.diccionarios', 'Wikctionary.dic'), 'a') as archivo:
                    archivo.write((palabra + '\n').encode('utf-8'))
            else:
                Wiktionary.diccionario_negativo.add(palabra)
                with open(resource_filename('clasificador.recursos.diccionarios', 'NoWikctionary.dic'), 'a') as archivo:
                    archivo.write((palabra + '\n').encode('utf-8'))
            return pertenece_palabra

    @staticmethod
    def pertenece_consulta(palabra):
        respuesta = requests.get('"https://en.wiktionary.org/w/api.php?' + urllib.urlencode({
            'action': 'opensearch',
            'search': palabra.encode('utf-8'),
        }))
        respuesta_json = json.loads(respuesta.text)
        return respuesta_json[0][3]
