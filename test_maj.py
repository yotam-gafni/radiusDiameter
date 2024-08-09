import time
import itertools
import random

d = 14
m = 27


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


for attempt in range(100):
	f = open("input_file1_d=12".format(random.choice([1,2,3,4,5])),"r+")
	f2 = open("input_file1_hadamard4".format(random.choice([1,2,3,4])),"r+")
	all_vecs1 = [elem.strip().replace(" ","")  for elem in f.readlines()]
	all_vecs2 = [elem.strip().replace(" ","")  for elem in f2.readlines()]
	random.shuffle(all_vecs2)
	all_vecs = []
	for i in range(len(all_vecs1)):
		all_vecs.append(all_vecs1[i] + all_vecs2[i])
	#maj = "?" * 2*d
	maj = find_maj([vec[:24] for vec in all_vecs]) + "?" * 3
	#maj = "?" * 20
	nice_print(all_vecs)
	print(maj)
	print(maj.count("?"))
	res, min_avg = calculate_diffs(all_vecs, maj)
	print("Is this an example? {}, the worst average is: {}".format(res,min_avg))
	if res:
		import pdb
		pdb.set_trace()
		nice_print(all_vecs)
