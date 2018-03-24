# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

import os

import numpy as np

try:
    # noinspection PyUnresolvedReferences
    import clasificador.config.environment
except ImportError:
    pass

# Twitter API credentials
CONSUMER_KEY = os.environ['CONSUMER_KEY']
CONSUMER_SECRET = os.environ['CONSUMER_SECRET']
ACCESS_KEY = os.environ['ACCESS_KEY']
ACCESS_SECRET = os.environ['ACCESS_SECRET']

# Whether to use MySQL or SQLite3

DB_ENGINE = os.environ['DB_ENGINE'] or 'mysql'

DB_HOST = os.environ['DB_HOST']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']
DB_NAME = os.environ['DB_NAME']
DB_NAME_CHISTES_DOT_COM = os.environ['DB_NAME_CHISTES_DOT_COM']

SUFIJO_PROGRESS_BAR = '%(index)#9d/%(max)#9d - %(percent)#6.2f%% - ETA: %(eta_td)s'


# Parametros para cada clasificador al realizar Grid Search

parameters_svm = {
    'C': [0.9, 1.0],
    'kernel': [str('rbf'), str('sigmoid'), str('poly'), str('linear')],
    'degree': [3, 4, 5],
    'gamma': [0.0, 0.03, 0.04, 0.05, 0.06],
    'coef0': [0.0, -1.0, 1.0]
}

parameters_dt = {
    'criterion': ['gini', 'entropy'],
    'splitter': ['best', 'random'],
    'max_features': range(17, 21),
    'max_depth': [None] + range(25, 30),
    'min_samples_split': range(1, 5),
    'min_samples_leaf': range(1, 4),
    'max_leaf_nodes': [None] + range(49, 52),
}

# No utiliza parametros
parameters_gnb = {

}

parameters_mnb = {
    'alpha': [i/10.0 for i in range(0, 21)],
    'fit_prior': [False, True]
}

parameters_knn = {
    'n_neighbors': [4, 5, 6, 7, 8],
    'weights': ['uniform', 'distance'],
    'p': [1, 2, np.inf]
}
