import random
import numpy as np

import sys

def readDataFromFile(file, keys = False):
	with open(file, 'r') as fileObj:
		if not keys:
			content = fileObj.readlines()[1:]
			content = [x.replace('\r\n', '').split(',') for x in content]
			content = [[float(x) if x != 'yes' and x != 'no' else 1 if x == 'yes' else 0 for x in y] for y in content]
		else:
			content = fileObj.readlines()
			content = [x.replace('\n', '') for x in content]
	return content

class NeuralNetwork():
	def __init__(self, training_example, lower_bound, upper_bound, eta = 0.05):
		self.training_example = training_example
		self.eta = eta
		self.attr_num = len(training_example[0]) - 1
		self.lower_bound = lower_bound
		self.upper_bound = upper_bound

		self.input_layer = NeuralLayer(attr_num=self.attr_num, hidden_layer=0)
		self.hidden_layer = NeuralLayer(attr_num=self.attr_num, hidden_layer=1)
		self.output_layer = NeuralLayer(hidden_layer= 2)
		self.layers = [self.input_layer, self.hidden_layer, self.output_layer]

		self.init_weight()  #Initialize every weight of every unit in the network

		self.training_example = self.normalize(self.training_example)

		self.training()

	def normalize(self, example, predict = False):
		attr_lb = self.lower_bound[:-1]
		attr_ub = self.upper_bound[:-1]
		result = []
		if not predict:
			for ex in example:
				temp = list((np.array(ex[:-1]) - np.array(attr_lb)) \
				            / (np.array(attr_ub) - np.array(attr_lb)))
				result.append(temp + [ex[-1] / 100.0])
			return result
		else:
			for ex in example:
				temp = list((np.array(ex) - np.array(attr_lb)) \
				            / (np.array(attr_ub) - np.array(attr_lb)))
				result.append(temp)
			return result

	def predicting(self, dev_example, dev_keys = None):
		temp = [el for el in dev_example]
		regularized = self.normalize(temp, True)
		for i, dev_ex in enumerate(regularized):
			for idx in range(self.layers[0].size):
				self.layers[0].units[idx].output = dev_ex[idx]
			for layer in range(1, len(self.layers)):
				for idx in range(0, self.layers[layer].size):
					net = self.compute_net(self.layers[layer - 1].units, idx)
					self.layers[layer].units[idx].output = 1 / (1 + np.exp(-net))
			output = self.layers[-1].units[0].output
			print output * 100

	def training(self):
		for _ in range(400):
			error = []
			for ex in self.training_example:
				for idx, unit in enumerate(self.layers[0].units):
					self.layers[0].units[idx].output = ex[idx]
				for layer in range(1, len(self.layers)):
					for idx in range(len(self.layers[layer].units)):
						net = self.compute_net(self.layers[layer - 1].units, idx)
						self.layers[layer].units[idx].output = 1.0 / (1 + np.exp(-net))
				output = self.layers[-1].units[0].output
				self.layers[-1].units[0].delta = output * (1 - output) * (ex[-1] - output)
				error.append((ex[-1] - output) ** 2)

				for layer in range(len(self.layers) - 2, -1, -1):
					for idx, unit in enumerate(self.layers[layer].units):
						self.layers[layer].units[idx].delta = unit.output * (1 - unit.output)\
						             * np.sum(np.array(unit.weights)\
						                      * np.array([u.delta for u in self.layers[layer + 1].units]))
						delta_w = np.array([u.delta for u in self.layers[layer + 1].units]) * self.eta * unit.output
						self.layers[layer].units[idx].weights = list(np.array(unit.weights) + np.array(delta_w))

			print 0.5 * sum(error)
		print 'TRAINING COMPLETED! NOW PREDICTING.'

	def compute_net(self, layer_units, index):
		w = [0 for _ in range(len(layer_units))]
		n = [0 for _ in range(len(layer_units))]
		for idx, unit in enumerate(layer_units):
			w[idx] = unit.weights[index]
			n[idx] = unit.output
		return np.sum(np.array(w) * np.array(n))

	def init_weight(self):
		"""Initialize weight for layers except output layer."""
		for layer in range(len(self.layers) - 1):
			for unit in self.layers[layer].units:
				unit.weights = [random.uniform(0, 1)\
				                for _ in range(self.layers[layer + 1].size)]

class NeuralLayer():
	def __init__(self, attr_num = 0, hidden_layer = 0):
		""" hidden_layer = 0: input layer
			hidden_layer = 1: hidden layer
			hidden_layer = 2: output layer
		"""
		self.units = []
		self.size = 0
		if not hidden_layer:
			self.units = [SigmoidUnit() for _ in range(attr_num)]
		elif hidden_layer == 2:
			self.units = [SigmoidUnit()]
		else:
			self.units = [SigmoidUnit() for _ in range(attr_num - 1)]
		self.size = len(self.units)

class SigmoidUnit():
	def __init__(self):
		self.weights = []
		self.output = 0
		self.delta = 0


# d_d_NN = NeuralNetwork(readDataFromFile('education_train.csv'), [0, 0, 0, 0, 0, 0], [100, 100, 100, 100, 100, 100], 0.091)
# d_d_NN.predicting(readDataFromFile('education_dev.csv'), readDataFromFile('education_dev_keys.txt', True))

assert len(sys.argv) == 3

training_file = sys.argv[1]
test_file = sys.argv[2]

d_d_NN = NeuralNetwork(readDataFromFile(training_file), [0, 0, 0, 0, 0, 0], [100, 100, 100, 100, 100, 100], 0.091)
d_d_NN.predicting(readDataFromFile(test_file))