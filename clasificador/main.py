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




	clasificados_positivos = 0
	son_positivos = 0

	verdaderos_positivos = 0
	falsos_positivos = 0

	verdaderos_negativos = 0
	falsos_negativos = 0

	precision = 0
	recall = 0
	accuracy = 0

	for tweet in evaluacion:
		clasificacion_es_humor = clasificador.predict(tweet.features.values())

		if clasificacion_es_humor:
			clasificados_positivos += 1

		if tweet.es_humor:
			son_positivos += 1

		if clasificacion_es_humor == tweet.es_humor:
			accuracy += 1

			if clasificacion_es_humor:
				verdaderos_positivos += 1
			else:
				verdaderos_negativos += 1
		else:
			if clasificacion_es_humor:
				falsos_positivos += 1
			else:
				falsos_negativos += 1

	if clasificados_positivos == 0:
		precision = 1.0
	else:
		precision = float(verdaderos_positivos)/clasificados_positivos

	if son_positivos == 0:
		recall = 1.0
	else:
		recall = float(verdaderos_positivos)/son_positivos

	accuracy = float(accuracy)/len(evaluacion)

	print('VP: ' + str(verdaderos_positivos))
	print('FP: ' + str(falsos_positivos))
	print('VN: ' + str(verdaderos_negativos))
	print('FN: ' + str(falsos_negativos))
	print
	print('Matriz de confusión:')
	print('\tP\tN')
	print('P\t' + str(verdaderos_positivos) + '\t' + str(falsos_positivos))
	print('N\t' + str(falsos_negativos) + '\t' + str(verdaderos_negativos))
	print
	print('Precision: ' + str(precision))
	print('Recall: ' + str(recall))
	print('Accuracy: ' + str(accuracy))
