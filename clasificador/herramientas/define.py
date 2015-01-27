# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

# Twitter API credentials
CONSUMER_KEY = 'GoJjP7Xmj4kpxjttr8qJ9cLtC'
CONSUMER_SECRET = 'PnbLJGXnJjsE9M97yhHXY2Oyj7ojcrcVulDGM2yQfS05NQjoNK'
ACCESS_KEY = '2714871673-HF7B4EPK4mWceAuEuBR4TRhJ12AGlJCVS6VPjZb'
ACCESS_SECRET = 'Yjp80IStjuot5Muvy4SAt2qoaHQdFGQDMJBqD4HQqX1s6'

DB_HOST = 'localhost'
DB_USER = 'pghumor'
DB_PASS = 'ckP8t/2l'
DB_NAME = 'corpus'
DB_NAME_CHISTES_DOT_COM = 'chistesdotcom'

SUFIJO_PROGRESS_BAR = '%(index)d/%(max)d - %(percent).2f%% - ETA: %(eta)ds'


# Parametros para cada clasificador al realizar Grid Search

parameters_svm = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_features': [None] + range(20, 25),
    'max_depth': [None] + range(25, 30),
    'min_samples_split': range(1, 5),
    'min_samples_leaf': range(1, 4),
    'max_leaf_nodes': [None] + range(49, 52),
}

parameters_dt = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_features': [None] + range(20, 25),
    'max_depth': [None] + range(25, 30),
    'min_samples_split': range(1, 5),
    'min_samples_leaf': range(1, 4),
    'max_leaf_nodes': [None] + range(49, 52),
}

parameters_gnb = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_features': [None] + range(20, 25),
    'max_depth': [None] + range(25, 30),
    'min_samples_split': range(1, 5),
    'min_samples_leaf': range(1, 4),
    'max_leaf_nodes': [None] + range(49, 52),
}

parameters_mnb = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_features': [None] + range(20, 25),
    'max_depth': [None] + range(25, 30),
    'min_samples_split': range(1, 5),
    'min_samples_leaf': range(1, 4),
    'max_leaf_nodes': [None] + range(49, 52),
}

parameters_knn = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_features': [None] + range(20, 25),
    'max_depth': [None] + range(25, 30),
    'min_samples_split': range(1, 5),
    'min_samples_leaf': range(1, 4),
    'max_leaf_nodes': [None] + range(49, 52),
}