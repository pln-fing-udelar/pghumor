# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn.ensemble import ExtraTreesClassifier
import sklearn.feature_selection as feature_selection


def tree_based_feature_selection(features, clases, corpus):
    print("Realizando tree-based feature selection")
    clf = ExtraTreesClassifier()
    clf.fit(features, clases)

    features_ordenadas = corpus[0].features_ordenadas()

    importancias = {}
    for i in range(len(features_ordenadas)):
        importancias[features_ordenadas[i]] = clf.feature_importances_[i]

    print("Ranking de features (Tree-based feature selection):\n")

    for nombre_feature in sorted(importancias, key=importancias.get, reverse=True):
        print(nombre_feature, importancias[nombre_feature])

    print("")
    print("")


def chi2_feature_selection(features, clases, features_ordenadas):
    print("Realizando chi2 feature selection")
    chi2_results = feature_selection.chi2(features, clases)

    importancias = {}
    for i in range(len(features_ordenadas)):
        importancias[features_ordenadas[i]] = chi2_results[0][i]

    print("Ranking de features (chi2):\n")

    for nombre_feature in sorted(importancias, key=importancias.get, reverse=True):
        print(nombre_feature, importancias[nombre_feature])

    print("")
    print("")


def f_score_feature_selection(features, clases, features_ordenadas):
    print("Realizando f-score feature selection")
    f_score = feature_selection.univariate_selection.f_classif(features, clases)

    importancias = {}
    for i in range(len(features_ordenadas)):
        importancias[features_ordenadas[i]] = f_score[0][i]

    print("Ranking de features (f-score):\n")

    for nombre_feature in sorted(importancias, key=importancias.get, reverse=True):
        print(nombre_feature, importancias[nombre_feature])

    print("")
    print("")