import time
import itertools
import random
import numpy

d = 16
m = 32


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


def test_all(all_vecs, maj_vec, max_dist):

	all_arr = numpy.array([[(int(elem)*2 - 1) for elem in vec] for vec in all_vecs])
	maj_lst = []
	for elem in maj_vec:
		if elem == "?":
			maj_lst.append(10)
		elif elem == "1":
			maj_lst.append(1)
		elif elem == "0":
			maj_lst.append(-1)
	maj_arr = numpy.array(maj_lst)

	s = time.time()
	counter = 0
	min_avg = d
	
	clear_maj_len = len(maj_vec) - maj_vec.count("?")
	no_clear_maj = maj_vec.count("?")
		
	clear_maj_indices = []

	for i in range(m):
		if maj_vec[i] != "?":
			clear_maj_indices.append(i) 
	print("Clear Majority Indices: {}".format(clear_maj_indices))

	for curr_dist in range(1, max_dist+1):
		print("CURR_DIST: {}".format(curr_dist))
		for in_comb in itertools.product([-1, 1], repeat=no_clear_maj):
			for out_comb in itertools.combinations(clear_maj_indices,curr_dist):
				if counter % 1000000 == 0:
					e = time.time()
					print(e - s)
					s = time.time()
				counter += 1
				out_lst = list(out_comb)
				#xor_dist_mask = numpy.array([1 if i in out_comb else 0 for i in range(m)])
				#new_maj_arr = numpy.bitwise_xor(maj_arr, xor_dist_mask)
				new_maj_arr = numpy.copy(maj_arr)
				new_maj_arr[out_lst] = - new_maj_arr[out_lst]
				new_maj_arr[new_maj_arr > 2] = in_comb
				diffs = numpy.dot(all_arr, new_maj_arr)
				import pdb
				pdb.set_trace()

				#diffs = [numpy.count_nonzero(arr != new_maj_arr) for arr in all_arr]
	return True, min_avg
					

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


f = open("input_file1_d=16".format(random.choice([1,2,3,4,5])),"r+")
all_vecs = [elem.strip().replace(" ","")  for elem in f.readlines()]
#maj = "?" * 2*d
maj = find_maj([vec for vec in all_vecs])
nice_print(all_vecs)
print(maj)
print(maj.count("?"))
res, min_avg = calculate_diffs(all_vecs, maj)
print("Is this an example? {}, the worst average is: {}".format(res,min_avg))

if len(all_vecs) %2 == 0:
	factor = 2
else:
	factor = 1

max_dist = int((d - 1 - min_avg) * len(all_vecs) / factor)
print(max_dist)
import pdb
pdb.set_trace()
res2, all_avg = test_all(all_vecs, maj, max_dist)
print("After testing relevant examples: {}, the worst average is: {}".format(res2,all_avg))
if res2:
	import pdb
	pdb.set_trace()
	nice_print(all_vecs)