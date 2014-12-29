# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import glob
from xml.etree import cElementTree as elementTree

from pkg_resources import resource_filename


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
    return [documento.text for documento in tree.findall('documento')]
