import time
import itertools
import random
import numpy

d = 16
m = 30


def find_maj(all_vecs):
	maj_vec = ""

	for i in range(len(all_vecs[0])):
		count0 = 0
		count1 = 0
		for j in range(len(all_vecs)):
			try:
				if all_vecs[j][i] == "0":
					count0 += 1
				else:
					count1 += 1
			except Exception as e:
				import pdb
				pdb.set_trace()
		if count0 > count1:
			maj_vec += "0"
		elif count1 > count0:
			maj_vec += "1"
		else: 
			maj_vec += "?"
	return maj_vec

def calculate_diffs(all_vecs, maj_vec):
	is_success = True
	lst = itertools.product([0, 1], repeat=maj_vec.count("?"))

	s = time.time()
	counter = 0
	min_avg = d
	for comb in lst:
		if counter % 100000 == 0:
			e = time.time()
			print(e - s)
			s = time.time()
		counter += 1
		new_maj_vec = ""
		count = 0
		for i in range(len(maj_vec)):
			if maj_vec[i] == "?":
				new_maj_vec += str(comb[count])
				count += 1
			else:
				new_maj_vec += maj_vec[i]
		#nice_print([new_maj_vec])
		diffs = [0 for vec in all_vecs]
		for i in range(len(new_maj_vec)):
			for j in range(len(all_vecs)):
				if all_vecs[j][i] != new_maj_vec[i]:
					diffs[j] += 1
		min_avg = min(min_avg, sum(diffs)/ len(diffs))
		#print(diffs)
		if max(diffs) < d:
			is_success = False
			print(diffs)
			nice_print([new_maj_vec])
			break
	return is_success, min_avg


def test_all(all_vecs):

	expected = []
	for i in range(16):
		ex_vec = []
		for j in range(16):
			if i != j:
				ex_vec.append(-1)
			else:
				ex_vec.append(15)
		expected.append(ex_vec)
	ex_arr = numpy.array(expected)

	all_arr = numpy.array([[(int(elem)*2 - 1) for elem in vec] for vec in all_vecs])

	s = time.time()
	counter = 0
	
	for in_comb in itertools.combinations(range(16), 8):
		for out_comb in itertools.combinations(range(16,30),7):
			if counter % 1000000 == 0:
				e = time.time()
				print(e - s)
				s = time.time()
			counter += 1
			idx_lst = list(in_comb + out_comb)
			diffs = numpy.dot(all_arr[:,idx_lst], all_arr[:,idx_lst].transpose())
			if numpy.array_equal(ex_arr, diffs):
				print("IT IS TWO HADAMARDS... Separating Index List: {}".format(idx_lst))
				return True
	return False
				

def nice_print(vecs):
	for vec in vecs:
		for i in range(len(vec)):
			if i % 4 == 3:
				print(vec[i], end="   ")
			else:
				print(vec[i], end="")
		print()

def arrange_final_vecs(final_vecs):
	new_final = []
	for i in range(m):
		all_zeros = True
		for vec in final_vecs: 
			if int(vec[i]) != 0:
				all_zeros = False
		if all_zeros:
			for vec in final_vecs:
				new_final.append(vec[:i])
			break
	if not all_zeros:
		new_final = final_vecs
	nice_print(new_final)
	return new_final


f = open("golden_d=16".format(random.choice([1,2,3,4,5])),"r+")
all_vecs = [elem.strip().replace(" ","")  for elem in f.readlines()]
res2 = test_all(all_vecs)
print("After testing relevant indices: {}".format(res2))
if res2:
	import pdb
	pdb.set_trace()
	nice_print(all_vecs)
