# coding=utf-8
from __future__ import absolute_import, division, print_function, unicode_literals
from collections import defaultdict
import itertools

from progress.bar import IncrementalBar
from sklearn.ensemble import ExtraTreesClassifier
import sklearn.feature_selection as feature_selection

from clasificador.herramientas.define import SUFIJO_PROGRESS_BAR
from clasificador.herramientas.freeling import Freeling
from clasificador.herramientas.persistencia import guardar_parecidos_con_distinto_humor, \
    cargar_parecidos_con_distinto_humor
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

    parecidos_con_distinto_humor = set()

    ids_parecidos_con_distinto_humor = cargar_parecidos_con_distinto_humor()

    if ids_parecidos_con_distinto_humor:
        corpus_por_id = {tweet.id: tweet for tweet in corpus}
        for id_tweet_humor, id_tweet_no_humor in ids_parecidos_con_distinto_humor:
            parecidos_con_distinto_humor.add((corpus_por_id[id_tweet_humor], corpus_por_id[id_tweet_no_humor]))
    else:
        subcorpus_cuentas_de_humor = []
        subsubcorpus_cuentas_de_humor_humor = []
        subsubcorpus_cuentas_de_humor_no_humor = []
        for tweet in corpus:
            if tweet.es_chiste:
                subcorpus_cuentas_de_humor.append(tweet)
                if tweet.es_humor:
                    subsubcorpus_cuentas_de_humor_humor.append(tweet)
                else:
                    subsubcorpus_cuentas_de_humor_no_humor.append(tweet)

        subsubcorpus_cuentas_de_humor_no_humor_por_largo = defaultdict(list)

        bar = IncrementalBar("Tokenizando\t\t\t", max=len(subcorpus_cuentas_de_humor),
                             suffix=SUFIJO_PROGRESS_BAR)
        bar.next(0)
        for tweet_cuenta_humor in subcorpus_cuentas_de_humor:
            tweet_cuenta_humor.oraciones = Freeling.procesar_texto(tweet_cuenta_humor.texto_original)
            tweet_cuenta_humor.tokens = list(itertools.chain(*tweet_cuenta_humor.oraciones))
            bar.next()
        bar.finish()

        for tweet_no_humor in subsubcorpus_cuentas_de_humor_no_humor:
            subsubcorpus_cuentas_de_humor_no_humor_por_largo[len(tweet_no_humor.tokens)].append(tweet_no_humor)

        bar = IncrementalBar("Buscando en tweets\t\t", max=len(subsubcorpus_cuentas_de_humor_humor),
                             suffix=SUFIJO_PROGRESS_BAR)
        bar.next(0)
        for tweet_humor in subsubcorpus_cuentas_de_humor_humor:
            margen = int(round(len(tweet_humor.tokens) / 5))
            largo_min = len(tweet_humor.tokens) - margen
            largo_max = len(tweet_humor.tokens) + margen

            for largo in range(largo_min, largo_max + 1):
                for tweet_no_humor in subsubcorpus_cuentas_de_humor_no_humor_por_largo[largo]:
                    if distancia_edicion(tweet_humor.tokens, tweet_no_humor.tokens)\
                            <= max(len(tweet_humor.tokens), len(tweet_no_humor.tokens)) / 5:
                        parecidos_con_distinto_humor.add((tweet_humor, tweet_no_humor))
                        print('')
                        print(tweet_humor.id)
                        print(tweet_humor.texto_original)
                        print("------------")
                        print(tweet_no_humor.id)
                        print(tweet_no_humor.texto_original)
                        print("------------")
                        print('')
            bar.next()
        bar.finish()

        guardar_parecidos_con_distinto_humor(parecidos_con_distinto_humor)

    return parecidos_con_distinto_humor


def mismas_features_distinto_humor(corpus):
    print("Buscando tweets con mismos valores de features pero distinto de humor...")

    humoristicos = [tweet for tweet in corpus if tweet.es_humor]
    no_humoristicos = [tweet for tweet in corpus if not tweet.es_humor]

    res = []

    bar = IncrementalBar("Buscando en tweets\t\t", max=len(humoristicos) * len(no_humoristicos),
                         suffix=SUFIJO_PROGRESS_BAR)
    bar.next(0)
    for tweet_humor in humoristicos:
        for tweet_no_humor in no_humoristicos:
            if tweet_humor.features == tweet_no_humor.features:
                res.append((tweet_humor, tweet_no_humor))
                if tweet_humor.texto_original == tweet_no_humor.texto_original:
                    print("-----MISMO TEXTO ORIGINAL------")
                if tweet_humor.texto == tweet_no_humor.texto:
                    print("----------MISMO TEXTO----------")
                if tweet_humor.id == tweet_no_humor.id:
                    print("-----------MISMO ID------------")
                if tweet_humor.cuenta == tweet_no_humor.cuenta:
                    print("----------MISMA CUENTA---------")
                print('')
                print(tweet_humor.id)
                print(tweet_humor.texto)
                print("------------")
                print(tweet_no_humor.id)
                print(tweet_no_humor.texto)
                print("------------")
                print('')
            bar.next()
    bar.finish()

    return res
