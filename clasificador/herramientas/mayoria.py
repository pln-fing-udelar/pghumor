#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from collections import defaultdict


class Mayoria():
    def __init__(self):
        self.mejor_clase = False
        pass

    def fit(self, X, y=None):
        clases_cantidad_dict = defaultdict(int)
        for valor_clase in y:
            clases_cantidad_dict[valor_clase] += 1
        self.mejor_clase = max(clases_cantidad_dict, key=lambda x: clases_cantidad_dict[x])
        return self

    def predict(self, X):
        return [self.mejor_clase for _ in X]
