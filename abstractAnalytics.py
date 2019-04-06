from abc import ABC, abstractclassmethod

class AbstractAnalytics(ABC):

	@abstractclassmethod
	def generatePNG(self):
		raise NotImplementedError('subclasses must override foo()!')

