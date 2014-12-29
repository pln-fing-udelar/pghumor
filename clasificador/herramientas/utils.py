# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import glob
import subprocess
import xml.etree.cElementTree as elementTree

from pkg_resources import resource_filename


def obtener_diccionario(filename):
    with open(filename) as archivo:
        lineas = []
        for linea in archivo:
            lineas.append(linea.decode('utf-8').rstrip('\n'))
        return lineas


def ejecutar_comando(command):
    while True:
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            return [linea.decode('utf-8') for linea in p.stdout.readlines()]
        except:
            # FIXME: habría que tomar una excepción más específica, ya que
            # no se puede salir por Ctrl + C del programa si está acá
            pass


def read_wiki_corpus():
    files = glob.glob(resource_filename('clasificador.recursos', 'wikicorpus/raw/*'))
    documentos = []
    for filename in files:
        documento = ""
        estado = 0
        with open(filename) as archivo:
            for linea in archivo:
                if linea == '\n' or linea == 'ENDOFARTICLE.\n':
                    continue
                if estado == 0:
                    if linea.startswith("<doc"):
                        documento = ""
                        estado = 1
                else:
                    if estado == 1:
                        if linea.startswith("</doc>"):
                            estado = 0
                            documentos.append(documento)
                        else:
                            documento += linea.decode('latin-1')
    return documentos


def obtener_sample_wikicorpus():
    tree = elementTree.parse(resource_filename('clasificador.recursos', 'wikicorpus_sample.xml'))
    documentos = []
    for documento in tree.findall('documento'):
        documentos.append(documento.text)
    return documentos
