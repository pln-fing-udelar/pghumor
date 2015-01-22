# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn.ensemble import ExtraTreesClassifier
import sklearn.feature_selection as feature_selection


def imprimir_importancias(feature_importances, nombre_metodo, nombres_features_ordenadas):
    importancias = {}
    for i in range(len(nombres_features_ordenadas)):
        importancias[nombres_features_ordenadas[i]] = feature_importances[i]

    print("Ranking de features ({nombre_metodo}):\n".format(nombre_metodo=nombre_metodo))

    for nombre_feature in sorted(importancias, key=importancias.get, reverse=True):
        print(nombre_feature, importancias[nombre_feature])

    print("")
    print("")


def tree_based_feature_selection(features, clases, nombres_features_ordenadas):
    print("Realizando tree-based feature selection")
    clf = ExtraTreesClassifier()
    clf.fit(features, clases)

    imprimir_importancias(clf.feature_importances_, "Tree-based feature selection", nombres_features_ordenadas)


def chi2_feature_selection(features, clases, nombres_features_ordenadas):
    print("Realizando chi2 feature selection")
    chi2_results = feature_selection.chi2(features, clases)

    imprimir_importancias(chi2_results[0], "chi2", nombres_features_ordenadas)


def f_score_feature_selection(features, clases, nombres_features_ordenadas):
    print("Realizando f-score feature selection")
    f_score = feature_selection.f_classif(features, clases)

    imprimir_importancias(f_score[0], "f-score", nombres_features_ordenadas)
