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

assert len(sys.argv) == 2

test = NaiveBayes(sys.argv[1], ['lib', 'con'])

for i in range(len(test.P_wv)):
	for w, p in islice(sorted(test.P_wv[i].items(), key=lambda x: x[1], reverse=True), 20):
		print w, '%.4f' % p
	print ''