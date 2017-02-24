from collections import Counter
from itertools import islice
from math import log
import sys

class NaiveBayes:
	def __init__(self, Examples, V, file_list = True):
		self.Examples = Examples
		self.V = V
		self.file_list = file_list

		self.Vocabulary = [Counter() for _ in range(len(self.V))]
		self.allVocabs = Counter()
		self.Pv = [0] * len(self.V)
		self.P_wv = [{} for _ in range(len(self.V))]

		self.preProcess()
		self.getP_wv()

	def preProcess(self):
		if self.file_list:
			files = self.readFiles()
			for file in files:
				words = self.readWords(file)
				self.Vocabulary[self.V.index(file[:3])].update(words)
				self.allVocabs.update(words)
				self.Pv[self.V.index(file[:3])] += 1
			self.Pv = [float(el) / len(files) for el in self.Pv]
		else:
			pass

	def stopWords(self, N):
		new_allVocabs = Counter(self.allVocabs)
		for w in islice(sorted(dict(new_allVocabs).items(), key=lambda x: x[1], reverse=True), N):
			for i in range(len(self.Vocabulary)):
				if w[0] in self.Vocabulary[i]:
					del self.Vocabulary[i][w[0]]
			del self.allVocabs[w[0]]
		self.P_wv = [{} for _ in range(len(self.V))]
		self.getP_wv()

	def getP_wv(self):
		for i in range(len(self.Vocabulary)):
			n = sum(self.Vocabulary[i].values())
			for w in self.allVocabs:
				self.P_wv[i][w] = (self.Vocabulary[i][w] + 1.0) / (n + len(self.allVocabs))

	def classify(self, doc):
		words = self.readWords(doc)
		temp = [0 for _ in range(len(self.V))]
		for i in range(len(self.Vocabulary)):
			temp[i] = log(self.Pv[i]) + sum([log(self.P_wv[i][w]) if w in self.allVocabs else 0 for w in words])
		return temp.index(max(temp))

	def readFiles(self):
		with open(self.Examples, 'r') as fileObj:
			files = [file.replace('\n', '') for file in fileObj.readlines()]
		return files

	def readWords(self, file):
		with open(file, 'r') as fileObj:
			words = [f.replace('\n', '').lower() for f in fileObj.readlines()]
		return words

class TestNB:
	def __init__(self, train_file, test_file, V, stopWords=None):
		self.train_file = train_file
		self.test_file = test_file
		self.V = V
		self.stopWords = stopWords

		self.NB = NaiveBayes(self.train_file, V)
		if stopWords:
			self.NB.stopWords(stopWords)

		self.accuracy = 0
		self.test_ins = self.readFiles()
		self.TRUE_LABEL = self.getTrueLabel()
		self.CLASSIFIED = []

		self.test()

		self.formatting()

	def test(self):
		files = self.test_ins
		for file in files:
			result = self.NB.classify(file)
			self.CLASSIFIED.append(self.V[result][0].upper())
		self.accuracy = sum([1.0 if self.CLASSIFIED[i] == self.TRUE_LABEL[i] else 0.0 for i in range(len(files))]) / len(files)

	def formatting(self):
		for label in self.CLASSIFIED:
			print label
		print 'Accuracy:', '%.4f' % self.accuracy

	def getTrueLabel(self):
		files = self.test_ins
		return [file[0].upper() for file in files]

	def readFiles(self):
		with open(self.test_file, 'r') as fileObj:
			files = [file.replace('\n', '') for file in fileObj.readlines()]
		return files

	def readWords(self, file):
		with open(file, 'r') as fileObj:
			words = [f.replace('\n', '').lower() for f in fileObj.readlines()]
		return words


assert len(sys.argv) == 4

TestNB(sys.argv[1], sys.argv[2], ['con', 'lib'], stopWords=int(sys.argv[3]))