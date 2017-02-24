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

def backward(dev_file, trans_file, emit_file, prior_file):
	dev = read_dev(dev_file)
	trans = read_trans(trans_file)
	emit = read_emit(emit_file)
	prior = read_prior(prior_file)
	result = []
	for sentence in range(len(dev)):
		beta_tp1 = {kT: 0 for kT in prior.keys()}
		beta_t = {}
		for word in range(len(dev[sentence]) - 1, 0, -1):
			for k in emit.keys():
				beta_t[k] = reduce(lambda x, y: log_sum(x, y), [v_tp1 + log(trans[k][k_tp1]) + log(emit[k_tp1][dev[sentence][word]]) for k_tp1, v_tp1 in beta_tp1.items()])
			beta_tp1 = dict(beta_t)
		result.append(reduce(lambda x, y: log_sum(x, y), [log(v1) + log(emit[k1][dev[sentence][0]]) + beta_tp1[k1] for k1, v1 in prior.items()]))
	print '\n'.join([str(x) for x in result])

# backward('dev.txt', 'hmm-trans.txt', 'hmm-emit.txt', 'hmm-prior.txt')

backward(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])