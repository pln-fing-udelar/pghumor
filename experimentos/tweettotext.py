# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals


class TweetToText():
    def __init__(self):
        pass

    def transform(self, tweets):
        return [tweet.texto for tweet in tweets]

    def fit(self, X, y=None):
        return self
