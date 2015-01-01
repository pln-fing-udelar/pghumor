#!/usr/bin/env python
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals


class TweetToText():
    def __init__(self):
        pass

    def transform(self, _tweets):
        return [_tweet.texto for _tweet in _tweets]

    def fit(self, X, y=None):
        return self
