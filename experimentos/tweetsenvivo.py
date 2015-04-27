#!/usr/bin/env python2
# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import HTMLParser
import json
import os
import sys

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from clasificador.herramientas.define import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET
from clasificador.realidad.tweet import patron_hashtag, patron_usuario, patron_url

COLOR_BLUE = '\033[94m'
COLOR_RED = '\033[91m'
COLOR_BG_RED = '\033[41m'
COLOR_YELLOW = '\033[93m'
COLOR_END = '\033[0m'


def colorear_texto(texto):
    sustituir_usuario = patron_usuario.sub(COLOR_YELLOW + r'\1' + COLOR_END, texto)
    sustituir_hashtag = patron_hashtag.sub(COLOR_RED + r'\1' + COLOR_END, sustituir_usuario)
    return patron_url.sub(COLOR_BG_RED + r'\1' + COLOR_END, sustituir_hashtag)


# Para ver localizaciones de tweets: http://www.tweetpaths.com/maps
class SalidaEstandarListener(StreamListener):
    def on_data(self, data):
        tweet = json.loads(data)
        texto = HTMLParser.HTMLParser().unescape(tweet["text"])
        usuario = tweet["user"]["screen_name"]
        print(COLOR_BLUE + usuario + COLOR_END)
        print(colorear_texto(texto))
        print('')
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = SalidaEstandarListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    stream = Stream(auth, listener)
    stream.filter(locations=[-56.435446, -34.938062, -56.016434, -34.698919])
    # Filtro sólo de Montevideo, sacado de: http://boundingbox.klokantech.com/
