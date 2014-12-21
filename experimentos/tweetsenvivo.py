#!/usr/bin/env python2
# coding=utf-8
from __future__ import absolute_import

import HTMLParser
import json

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

CONSUMER_KEY = "GoJjP7Xmj4kpxjttr8qJ9cLtC"
CONSUMER_SECRET = "PnbLJGXnJjsE9M97yhHXY2Oyj7ojcrcVulDGM2yQfS05NQjoNK"

ACCESS_TOKEN = "2714871673-HF7B4EPK4mWceAuEuBR4TRhJ12AGlJCVS6VPjZb"
ACCESS_TOKEN_SECRET = "Yjp80IStjuot5Muvy4SAt2qoaHQdFGQDMJBqD4HQqX1s6"


class SalidaEstandarListener(StreamListener):
    def on_data(self, data):
        tweet = HTMLParser.HTMLParser().unescape(json.loads(data))
        print(tweet["text"])
        print('')
        return True

    def on_error(self, status):
        print(status)


if __name__ == '__main__':
    listener = SalidaEstandarListener()
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

    stream = Stream(auth, listener)
    stream.filter(locations=[-56.435446, -34.938062, -56.016434, -34.698919])  # http://boundingbox.klokantech.com/
