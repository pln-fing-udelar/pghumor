#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import

import random
from sklearn import svm

import clasificador.herramientas.persistencia
from clasificador.features.features import Features

import argparse


corpus = []

entrenamiento = []
evaluacion = []

clasificador_usado = svm.SVC()

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('--recalcular-features', action='store_true', default=False)
	parser.add_argument('--recalcular-feature', type=str)
	parser.add_argument('--limit', type=int)

	args = parser.parse_args()

	corpus = clasificador.herramientas.persistencia.cargar_tweets()

	if args.limit is not None:
		elegir_algunos = random.sample(range(len(corpus)), args.limit)
		corpus = [corpus[i] for i in range(len(corpus)) if i in elegir_algunos]

	if args.recalcular_features:
		features_obj = Features()
		features_obj.calcular_features(corpus)
		clasificador.herramientas.persistencia.guardar_features(corpus)
	elif args.recalcular_feature is not None:
		features_obj = Features()
		features_obj.calcular_feature(corpus, args.recalcular_feature)
		clasificador.herramientas.persistencia.guardar_features(corpus)

	fraccion_evaluacion = .1

	print(corpus[1].texto)

	elegir_fraccion = random.sample(range(len(corpus)), int(len(corpus) * fraccion_evaluacion))
	entrenamiento = [corpus[i] for i in range(len(corpus)) if i not in elegir_fraccion]
	evaluacion = [corpus[i] for i in elegir_fraccion]

	features_entrenamiento = [tweet.features.values() for tweet in entrenamiento]

	grupos_entrenamiento = [tweet.es_humor for tweet in entrenamiento]

	clasificador_usado.fit(features_entrenamiento, grupos_entrenamiento)

	# Reporte de estadísticas

	verdaderos_positivos = []
	falsos_positivos = []

	verdaderos_negativos = []
	falsos_negativos = []

	for tweet in evaluacion:
		clasificacion_es_humor = clasificador_usado.predict(tweet.features.values())

		if clasificacion_es_humor == tweet.es_humor:
			if clasificacion_es_humor:
				verdaderos_positivos.append(tweet)
			else:
				verdaderos_negativos.append(tweet)
		else:
			if clasificacion_es_humor:
				falsos_positivos.append(tweet)
			else:
				falsos_negativos.append(tweet)

	if len(verdaderos_positivos) + len(falsos_positivos) == 0:
		precision = 1.0
	else:
		precision = float(len(verdaderos_positivos)) / (len(verdaderos_positivos) + len(falsos_positivos))

	if len(verdaderos_positivos) + len(falsos_negativos) == 0:
		recall = 1.0
	else:
		recall = float(len(verdaderos_positivos)) / (len(verdaderos_positivos) + len(falsos_negativos))

	accuracy = float(len(verdaderos_positivos) + len(verdaderos_negativos)) / len(evaluacion)

	print('VP: ' + str(len(verdaderos_positivos)))
	print('FP: ' + str(len(falsos_positivos)))
	print('VN: ' + str(len(verdaderos_negativos)))
	print('FN: ' + str(len(falsos_negativos)))
	print()
	print('Matriz de confusión:')
	print('\tP\tN')
	print('P\t' + str(len(verdaderos_positivos)) + '\t' + str(len(falsos_positivos)))
	print('N\t' + str(len(falsos_negativos)) + '\t' + str(len(verdaderos_negativos)))
	print()
	print('Precision: ' + str(precision))
	print('Recall: ' + str(recall))
	print('Accuracy: ' + str(accuracy))
