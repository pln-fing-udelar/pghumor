# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
import itertools

from progress.bar import IncrementalBar
from sklearn.ensemble import ExtraTreesClassifier
import sklearn.feature_selection as feature_selection

from clasificador.herramientas.define import SUFIJO_PROGRESS_BAR
from clasificador.herramientas.freeling import Freeling
from clasificador.herramientas.utils import distancia_edicion


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
    clf = ExtraTreesClassifier(n_estimators=1000)
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


def tweets_parecidos_con_distinto_humor(corpus):
    print("Buscando tweets muy parecidos pero con distinto valor de humor...")

    subcorpus_humor = [tweet for tweet in corpus if tweet.es_chiste]

    subcorpus_humor_por_largo = defaultdict(list)

    bar = IncrementalBar("Tokenizando\t\t\t", max=len(subcorpus_humor), suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)
    for tweet in subcorpus_humor:
        tweet.oraciones = Freeling.procesar_texto(tweet.texto_original)
        tweet.tokens = list(itertools.chain(*tweet.oraciones))

        subcorpus_humor_por_largo[len(tweet.tokens)].append(tweet)

        bar.next()

    bar.finish()

    parecidos_con_distinto_humor = set()

    bar = IncrementalBar("Buscando en tweets\t\t", max=len(subcorpus_humor), suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)
    i = 1
    for tweet1 in subcorpus_humor:
        margen = int(round(len(tweet1.tokens) / 5))
        largo_min = len(tweet1.tokens) - margen
        largo_max = len(tweet1.tokens) + margen

        for largo in range(largo_min, largo_max + 1):
            for tweet2 in subcorpus_humor_por_largo[largo]:
                if tweet1.id < tweet2.id:
                    if tweet1.es_humor != tweet2.es_humor \
                            and distancia_edicion(tweet1.tokens, tweet2.tokens) \
                                    <= max(len(tweet1.tokens), len(tweet2.tokens)) / 5:
                        parecidos_con_distinto_humor.add(tweet1)
                        parecidos_con_distinto_humor.add(tweet2)
                        print('')
                        print(tweet1.id)
                        print(tweet1.texto_original)
                        print("------------")
                        print(tweet2.id)
                        print(tweet2.texto_original)
                        print("------------")
                        print('')
        bar.next()
    bar.finish()

    return parecidos_con_distinto_humor


def mismas_features_distinto_humor(corpus):
    print("Buscando tweets con mismos valores de features pero distinto de humor...")

    humoristicos = [tweet for tweet in corpus if tweet.es_humor]
    no_humoristicos = [tweet for tweet in corpus if not tweet.es_humor]

    bar = IncrementalBar("Buscando en tweets", max=len(humoristicos) * len(no_humoristicos),
                         suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)
    for tweet1 in humoristicos:
        for tweet2 in no_humoristicos:
            if tweet1.features == tweet2.features:
                if tweet1.texto_original == tweet2.texto_original:
                    print("-----MISMO TEXTO ORIGINAL------")
                if tweet1.texto == tweet2.texto:
                    print("----------MISMO TEXTO----------")
                if tweet1.id == tweet2.id:
                    print("-----------MISMO ID------------")
                if tweet1.cuenta == tweet2.cuenta:
                    print("----------MISMA CUENTA---------")
                print('')
                print(tweet1.id)
                print(tweet1.texto)
                print("------------")
                print(tweet2.id)
                print(tweet2.texto)
                print("------------")
                print('')
            bar.next()
    bar.finish()
