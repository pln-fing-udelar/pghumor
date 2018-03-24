# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os

# Twitter API credentials
os.environ['CONSUMER_KEY'] = ''
os.environ['CONSUMER_SECRET'] = ''
os.environ['ACCESS_KEY'] = ''
os.environ['ACCESS_SECRET'] = ''

os.environ['DB_ENGINE'] = 'sqlite3'

os.environ['DB_HOST'] = 'localhost'
os.environ['DB_USER'] = 'pghumor'
os.environ['DB_PASS'] = ''
os.environ['DB_NAME'] = 'corpus.sqlite3'
os.environ['DB_NAME_CHISTES_DOT_COM'] = 'chistesdotcom.sqlite3'
