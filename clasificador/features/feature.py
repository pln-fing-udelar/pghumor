from __future__ import absolute_import

import abc

class Feature:
	__metaclass__ = abc.ABCMeta
	
	def __init__(self):
		self.nombre = ""
		self.descripcion = ""


	@abc.abstractmethod
	def calcularFeature(self, tweet):
		"""Calcula la feature para el tweet y le asigna su valor al mismo"""
		return
