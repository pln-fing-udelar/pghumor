# coding=utf-8
from __future__ import absolute_import, division, unicode_literals

import subprocess
import glob
import xml.etree.cElementTree as ET


def obtener_diccionario(filename):
    lines = [line.decode('utf-8').rstrip('\n') for line in open(filename)]
    return lines


def ejecutar_comando(command):
    while True:
        try:
            p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            p.wait()
            return [_str.decode('utf-8') for _str in p.stdout.readlines()]
        except:
            pass


def read_wiki_corpus():
    files = glob.glob("clasificador/recursos/wikicorpus/raw/*")
    documentos = []
    for filename in files:
        documento = ""
        estado = 0
        with open(filename) as f:
            for line in f.readlines():
                if line == '\n' or line == 'ENDOFARTICLE.\n':
                    continue
                if estado == 0:
                    if line.startswith("<doc"):
                        documento = ""
                        estado = 1
                else:
                    if estado == 1:
                        if line.startswith("</doc>"):
                            estado = 0
                            documentos.append(documento)
                        else:
                            documento += line.decode('latin-1')

    return documentos


def obtener_sample_wikicorpus():
    tree = ET.parse('clasificador/recursos/wikicorpus_sample.xml')
    documentos = []
    for documento in tree.findall('documento'):
        documentos.append(documento.text)

    return documentos
