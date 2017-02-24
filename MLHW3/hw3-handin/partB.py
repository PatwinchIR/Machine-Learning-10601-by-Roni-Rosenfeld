import sys

assert len(sys.argv) == 2

_value_1 = ["Male", "Young", "Yes", "Yes", "high\r\n"]
_value_0 = ["Female", "Old", "No", "No", "low\r\n"]
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
	D = []
	for i in data:
		D.append(int("".join([str(v) for v in i]), 2))
	bit_mani = []
	for inst in D:
		result = inst & 1
		x_data = inst >> 1
		bit_mani.append((x_data, result))
	return bit_mani

"""====Task 1, 2===="""
print pow(2, 4)
print pow(2, pow(2, 4))

"""====Task 3===="""
bit_mani = read_data_from_file("4Cat-Train.labeled")

VS = []
for i in range(65536):
	VS.append(i)

final_VS = []
for hypo in VS:
	in_cons = False
	for ls_bits, result in bit_mani:
		if (hypo >> (15 - ls_bits)) & 1 != result:
			in_cons = True
			break
	if not in_cons:
		final_VS.append(hypo)

#print final_VS

"""====Task 4===="""
print len(final_VS)
true_data = read_data_from_file(sys.argv[1])
for ls_bits, result in true_data:
	vote = 0
	for hypo in final_VS:
		if (hypo >> (15 - ls_bits)) & 1 == result:
			vote += 1
	if result == 1:
		print " ".join(str(x) for x in [vote, len(final_VS) - vote])
	else:
		print " ".join(str(x) for x in [len(final_VS) - vote, vote])