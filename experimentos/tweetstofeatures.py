#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from clasificador.herramientas.utilclasificacion import get_features


class TweetsToFeatures():
    def __init__(self):
        pass

    def transform(self, _tweets):
        return get_features(_tweets)

    def fit(self, X, y=None):
        return self
