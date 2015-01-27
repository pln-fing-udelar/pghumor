# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals

from sklearn.ensemble import ExtraTreesClassifier
import sklearn.feature_selection as feature_selection


def imprimir_importancias(feature_importances, nombre_metodo, nombres_features_ordenadas):
    if len(feature_importances) == 2:
        p_valores = feature_importances[1]
        feature_importances = feature_importances[0]
    else:
        p_valores = None

    importancias = {}
    p_valores_dict = {}
    for i in range(len(nombres_features_ordenadas)):
        importancias[nombres_features_ordenadas[i]] = feature_importances[i]
        if p_valores is not None:
            p_valores_dict[nombres_features_ordenadas[i]] = p_valores[i]

    print("Ranking de features ({nombre_metodo}):\n".format(nombre_metodo=nombre_metodo))

    for nombre_feature in sorted(importancias, key=importancias.get, reverse=True):
        if p_valores is None:
            print(nombre_feature, importancias[nombre_feature])
        else:
            print(nombre_feature, importancias[nombre_feature], p_valores_dict[nombre_feature])

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

    imprimir_importancias(chi2_results, "chi2", nombres_features_ordenadas)


def f_score_feature_selection(features, clases, nombres_features_ordenadas):
    print("Realizando f-score feature selection")
    f_score = feature_selection.f_classif(features, clases)

    imprimir_importancias(f_score, "f-score", nombres_features_ordenadas)
