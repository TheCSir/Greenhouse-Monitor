from abc import ABC, abstractclassmethod

class AbstractAnalytics(ABC):

	@abstractclassmethod
	def generate_PNG(self):
		raise NotImplementedError('Must override method generate_PNG()')

