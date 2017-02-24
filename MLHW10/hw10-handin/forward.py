from logsum import log_sum
from math import log
import sys

def read_emit(emit_file):
	with open(emit_file, 'r') as fileObj:
		content = [x.replace('\n', '') for x in fileObj.readlines()]
		emit = {}
		for el in content:
			name = el[:2]
			prob = dict(map(lambda u: [u.split(':')[0], float(u.split(':')[1])], [x for x in el[2:].split(' ')[1:] if x]))
			emit[name] = prob
		return emit

def read_trans(trans_file):
	with open(trans_file, 'r') as fileObj:
		content = [x.replace('\n', '').split(' ') for x in fileObj.readlines()]
		trans = {}
		for li in content:
			name = li[0]
			prob = dict(map(lambda u: [u.split(':')[0], float(u.split(':')[1])], [x for x in li[1:] if x]))
			trans[name] = prob
		return trans

def read_prior(prior_file):
	with open(prior_file, 'r') as fileObj:
		content = [x.replace('\n', '') for x in fileObj.readlines()]
		prior = dict(map(lambda u: [u.split(' ')[0], float(u.split(' ')[1])], [x for x in content]))
		# print sum(prior.values())
		return prior

def read_dev(dev_file):
	with open(dev_file, 'r') as fileObj:
		content = [x.replace('\n', '').split(' ') for x in fileObj.readlines()]
		# print content
		return content

def forward(dev_file, trans_file, emit_file, prior_file):
	dev = read_dev(dev_file)
	trans = read_trans(trans_file)
	emit = read_emit(emit_file)
	prior = read_prior(prior_file)
	result = []
	for sentence in range(len(dev)):
		alpha_t = {k1: log(v1) + log(emit[k1][dev[sentence][0]]) for k1, v1 in prior.items()}
		alpha_tp1 = {}
		for word in range(1, len(dev[sentence])):
			for k in emit.keys():
				alpha_tp1[k] = log(emit[k][dev[sentence][word]]) + reduce(lambda x, y: log_sum(x, y), [tv + log(trans[tk][k]) for tk, tv in alpha_t.items()])
			alpha_t = dict(alpha_tp1)
		result.append(reduce(lambda x, y: log_sum(x, y), alpha_t.values()))
	print '\n'.join([str(x) for x in result])



# forward('dev.txt', 'hmm-trans.txt', 'hmm-emit.txt', 'hmm-prior.txt')

forward(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])