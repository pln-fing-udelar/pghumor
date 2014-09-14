#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from sklearn import svm

import herramientas.cargardatos
#import features.features
import herramientas.tokenizacion

#def recolectarFeatures(tweets):
#	return [obtenerFeaturePalabrasSexuales(tweets), obtenerFeaturePalabrasAnimales(tweets), obtenerFeaturePalabrasPersonal(tweets)]

#def darFeatures(*features):
#	return [list(tupla) for tupla in zip(*features)]

humor, no_humor = herramientas.cargardatos.extraerTweets()

corpus = humor + no_humor

elegir10 = random.sample(range(len(corpus)), int(len(corpus)*.1))
entrenamiento = [corpus[i] for i in range(len(corpus)) if i not in elegir10]
evaluacion = [corpus[i] for i in elegir10]

#tweets_tokenizados = [tokenizacion.tokenizar(tweet.texto) for tweet in tweets]

#features = darFeatures(recolectarFeatures(entrenamiento))
features = []
i = 0
for tweet in entrenamiento:
	features_tweet = []
	if entrenamiento[i].texto.find('sexo') == -1:
		features_tweet.append(0)
	else:
		features_tweet.append(1)
	features.append(features_tweet)

grupos = [tweet.es_humor for tweet in entrenamiento]

clasificador = svm.SVC()
clasificador.fit(features, grupos)

#clasificador.predict(evaluacion[0])
