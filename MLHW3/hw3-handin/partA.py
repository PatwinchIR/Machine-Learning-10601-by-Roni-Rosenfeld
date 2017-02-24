import sys

assert len(sys.argv) == 2

"""
Gender             Male  1    Female 0
Age                Young 1    Old    0
Student            Yes   1    No     0
PreviouslyDeclined Yes   1    No     0
HairLength         Long  1    Short  0
Employed           Yes   1    No     0
TypeOfColateral    House 1    Car    0
FirstLoan          Yes   1    No     0
LifeInsurance      Yes   1    No     0
======================================
Risk               High  1    Low    0
"""

_value_1 = ["Male", "Young", "Yes", "Yes", "Long", "Yes", "House", "Yes", "Yes", "high\r\n"]
_value_0 = ["Female", "Old", "No", "No", "Short", "No", "Car", "No", "No", "low\r\n"]
def read_data_from_file(file_name):
	with open(file_name, 'r') as file_object:
		content = file_object.readlines()
	instances = []
	for inst in content:
		instances.append(inst.split("\t"))
	data = []
	for inst in instances:
		item = []
		for attr in inst:
			item.append(1 if attr.split(" ")[1] in _value_1 else 0)
		data.append(item)
	return data

"""====Task 1, 2, 3===="""
print pow(2, 9)
print len(str(pow(2, pow(2, 9))))
print pow(3, 9) + 1

"""====Task 4===="""
hypos = []
hypo = []
count = 0
for inst in read_data_from_file("9Cat-Train.labeled"):
	count += 1
	if inst[-1] == 1:
		d = inst[:-1]
		hypo = d if not hypo else map(lambda x, y: x if x == y else -1, hypo, d)
	if count%30 == 0:
		hypos.append(hypo)

result = []
for h in hypos:
	result.append(map(lambda x, y, z: y if x == 1 else z if x == 0 else "?", h, _value_1[:-1], _value_0[:-1]))

with open('partA4.txt', 'w') as output:
	for r in result:
		output.writelines("\t".join(r) + '\n')

"""====Task 5===="""
def get_predict(instance, hypo):
	global _value_0
	global _value_1
	new_hypo = map(lambda x, y, z: 1 if x == y else 0 if x == z else -1, hypo, _value_1[:-1], _value_0[:-1])
	for i in range(len(new_hypo)):
		if new_hypo[i] == -1:
			continue
		elif new_hypo[i] != instance[i]:
			return 0
	return 1

with open('partA4.txt', 'r') as HYPO_file:
	final_hypo = HYPO_file.readlines()[-2].strip("\n").split("\t")

miss = 0.0
all = 0.0
for inst in read_data_from_file("9Cat-Dev.labeled"):
	all += 1
	predict = get_predict(inst[:-1], final_hypo)
	if predict != inst[-1]:
		miss += 1

print miss/all

"""====Task 6===="""
input = read_data_from_file(sys.argv[1])
for i in input:
	result = get_predict(i, final_hypo)
	print ("high" if result == 1 else "low")


