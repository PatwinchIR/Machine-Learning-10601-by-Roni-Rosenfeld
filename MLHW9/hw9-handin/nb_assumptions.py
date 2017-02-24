from collections import Counter

import sys

class NaiveBayes:
	def __init__(self, file):
		self.file = file

		self.Data = self.readData(self.file)
		self.labelData = [[] for _ in range(2)]
		self.all = [[Counter() for _ in range(len(self.Data[0]) - 1)] for _ in range(2)]

		self.Pv = [0] * 2
		self.P_wv = [[{} for _ in range(len(self.Data[0]) - 1)] for _ in range(2)]
		self.P_evi = [0 for _ in range(len(self.Data[0]) - 1)]

		self.preProcess()
		self.getP_wv()

	def readData(self, file):
		with open(file, 'r') as fileObj:
			data = [line.replace('\n', '').split(' ') for line in fileObj.readlines()]
		return data

	def preProcess(self):
		for data in self.Data:
			self.labelData[int(data[-1])].append(data)
		for i in range(len(self.labelData)):
			new_data = zip(*self.labelData[i])[:-1]
			for j, data in enumerate(new_data):
				self.all[i][j].update(data)
		tr = zip(*self.Data)[:-1]
		self.P_evi = [sum([float(el) for el in item]) / len(tr[0]) for item in tr]

	def getP_wv(self):
		self.Pv = [float(len(self.labelData[i])) / (len(self.labelData[0]) + len(self.labelData[1])) for i in range(len(self.labelData))]
		for r in range(len(self.all)):
			for f in range(len(self.all[r])):
				self.P_wv[r][f]['0'] = float(self.all[r][f]['0']) / sum(self.all[r][f].values())
				self.P_wv[r][f]['1'] = float(self.all[r][f]['1']) / sum(self.all[r][f].values())

	def getResult(self, file):
		data = self.readData(file)
		for d in data:
			result = self.Pv[1] * reduce((lambda x, y: float(x) * y), [self.P_wv[1][j][str(d[j])] for j in range(len(d[:-1]))]) / reduce((lambda x, y: x * y), [self.P_evi[k] if int(d[k]) else 1 - self.P_evi[k] for k in range(len(d[:-1]))])
			print result

assert len(sys.argv) == 3

test = NaiveBayes('naive_assumption/' + sys.argv[1])
test.getResult('naive_assumption/' + sys.argv[2])