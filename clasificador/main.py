#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from sklearn import svm

import herramientas.cargardatos
from features.features import Features

corpus = []

entrenamiento = []
evaluacion = []

clasificador = svm.SVC()

if __name__ == "__main__":
	humor, no_humor = herramientas.cargardatos.extraerTweets()

	corpus = humor + no_humor

	features_obj = Features()
	features_obj.calcularFeatures(corpus)

	fraccion_evaluacion = .1

	elegir10 = random.sample(range(len(corpus)), int(len(corpus)*fraccion_evaluacion))
	entrenamiento = [corpus[i] for i in range(len(corpus)) if i not in elegir10]
	evaluacion = [corpus[i] for i in elegir10]

	features_entrenamiento = [tweet.features.values() for tweet in entrenamiento]

	grupos_entrenamiento = [tweet.es_humor for tweet in entrenamiento]

	clasificador.fit(features_entrenamiento, grupos_entrenamiento)

	#clasificador.predict(evaluacion[0].features.values())
