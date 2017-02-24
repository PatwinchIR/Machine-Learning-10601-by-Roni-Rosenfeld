import sys
import math

assert len(sys.argv) == 3
train_file = sys.argv[1]
test_file = sys.argv[2]

def read_data_from_file(filename):
	positive = ["democrat", "A", "y", "before1950", "yes", "morethan3min", "fast", "expensive",
	            "high", "Two", "large"]
	with open(filename) as file_obj:
		content = file_obj.readlines()
	content = [x.strip("\r\n") for x in content]
	content = [x.strip("\n") for x in content]
	content = [x.replace(" ", "") for x in content]
	attr_name = content[0].split(",")
	attr_val = [[1 if a in positive else 0 for a in inst.split(",")] for inst in content[1:]]
	return (attr_name, attr_val)

def entropy(Array):
	sum = 0
	for x in Array:
		sum += x
	if sum == 0 or sum == len(Array):
		return 0
	p = float(sum) / len(Array)
	return - p * math.log(p, 2) - (1 - p) * math.log(1 - p, 2)

class Node:
	def __init__(self, entropy, label = 1, attr = -1, l = None, r = None):
		self.entropy = entropy
		self.l = l
		self.r = r
		self.label = label
		self.attr = attr
		self.pos = 0
		self.neg = 0
		self.fattr = -1
		self.mi = 0

def get_best(en, Ex, Attr):
	pool = []
	for attr in Attr:
		pos_temp = []
		neg_temp = []
		for ex in Ex:
			if ex[attr] == 1:
				pos_temp.append(ex[-1])
			else:
				neg_temp.append(ex[-1])
		pool.append(en - len(pos_temp)/float(len(Ex)) * entropy(pos_temp) - len(neg_temp)/float(len(Ex)) * entropy(neg_temp))
	return (max(pool), Attr[pool.index(max(pool))])

def ID3(Examples, Attributes, attr):
	pos = 0
	for ex in Examples:
		pos += ex[-1]
	if pos == 0 or pos == len(Examples):
		root = Node(0)
		root.pos = pos
		root.neg = len(Examples) - pos
		root.attr = attr
		if pos == 0:
			root.label = 0
		elif pos == len(Examples):
			root.label = 1
		return root
	frac = float(pos) / len(Examples)
	root = Node(- frac * math.log(frac, 2) - (1 - frac) * math.log(1 - frac, 2))
	root.pos = pos
	root.neg = len(Examples) - pos
	root.attr = attr
	root.label = 0 if pos <= len(Examples) / 2 else 1

	if len(Attributes) == 0:
		root.label = 0 if pos <= len(Examples)/2 else 1
		return root
	else:
		root.mi, A = get_best(root.entropy, Examples, Attributes)
		root.fattr = A
		new_exl = []
		new_exr = []
		for ex in Examples:
			if ex[A] == 1:
				new_exl.append(ex)
			else:
				new_exr.append(ex)
		if len(new_exl) == 0:
			root.label = 0 if pos <= len(Examples) / 2 else 1
			return root
		if len(new_exr) == 0:
			root.label = 0 if pos <= len(Examples) / 2 else 1
			return root
		new_attr = [attr for attr in Attributes if attr != A]
		if root.mi >= 0.1:
			root.l = ID3(new_exl, new_attr, A)
			root.r = ID3(new_exr, new_attr, A)
	return root

def preO(root, l, depth):
	if root == None or depth >= 3:
		return
	print_out = ""
	if depth == 0:
		print_out += "[" + str(root.pos) + "+/" + str(root.neg) + "-]"
	else:
		if depth > 1:
			print_out += "| "
		if l == 1:
			print_out += train_name[root.attr] + " = y: [" + str(root.pos) + "+/" + str(root.neg) + "-]"
		else:
			print_out += train_name[root.attr] + " = n: [" + str(root.pos) + "+/" + str(root.neg) + "-]"
	print print_out
	preO(root.l, 1, depth + 1)
	preO(root.r, 0, depth + 1)

current = []
def get_pred(root, ex, depth):
	global current
	if root == None or depth >= 3:
		return
	if ex[root.fattr] == 1:
		current.append(root.label)
		get_pred(root.l, ex, depth + 1)
	else:
		current.append(root.label)
		get_pred(root.r, ex, depth + 1)

error_train = 0.0
train_name, train_val = read_data_from_file(train_file)
attr_num = len(train_name) - 1

root = ID3(train_val, [x for x in range(attr_num)], -1)
preO(root, -1, 0)

for ex in train_val:
	current = []
	get_pred(root, ex, 0)
	if current[-1] != ex[-1]:
		error_train += 1

error_test = 0.0
test_name, test_val = read_data_from_file(test_file)
for ex in test_val:
	current = []
	get_pred(root, ex, 0)
	if current[-1] != ex[-1]:
		error_test += 1

print "error(train): " + str(error_train / len(train_val))
print "error(test): " + str(error_test / len(test_val))
