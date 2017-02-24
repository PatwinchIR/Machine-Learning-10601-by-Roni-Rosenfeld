import sys

assert len(sys.argv) == 2
file_name = sys.argv[1]

import math
def read_data_from_file(filename):
	positive = ["democrat", "A", "y", "before1950", "yes", "morethan3min", "fast", "expensive",
	            "high", "Two", "large"]
	with open(filename) as file_obj:
		content = file_obj.readlines()
	content = [x.strip("\r\n") for x in content]
	content = [x.strip("\n") for x in content]
	content = [x.strip(" ") for x in content]
	attr_name = content[0].split(", ")
	attr_val = [['1' if a in positive else '0' for a in inst.split(",")] for inst in content[1:]]
	result = []
	for x in attr_val:
		result.append([int(''.join(x), 2) >> 1, int(x[-1])])
	return (attr_name, result)

example_name, example_val = read_data_from_file(file_name)
positive = 0
for el in example_val:
	positive += el[-1]
entropy = 0.0
frac = 0.0
if positive != 0 and positive != len(example_val):
	frac = float(positive) / len(example_val)
	entropy = - frac * math.log(frac, 2) - (1 - frac) * math.log(1 - frac, 2)
elif positive == 0:
	frac = 0.0
	entropy = 0.0
else:
	frac = 1.0
	entropy = 0.0
print "entropy:", entropy
print "error:", frac if frac < 0.5 else 1 - frac