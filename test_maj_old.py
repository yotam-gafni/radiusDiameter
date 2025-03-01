import time
import itertools
import random

d = 14
m = 28


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
	counter_13 = 0
	all_singletons = set([])
	all_doubles = set([])
	all_triples = set([])
	all_quartets = set([])
	for i in [1,6,7,12,13,14,15]:
		for j in [1,6,7,12,13,14,15]:
			if i<j:
				all_doubles.add(tuple([i,j]))

	allowed_doubles = {(6, 12), (6, 15), (1, 12), (13, 14), (1, 15), (6, 14), (7, 13), (12, 15), (1, 14), (6, 13), (7, 12), (7, 15), (12, 14), (1, 13), (13, 15), (7, 14)}
	allowed_triples = {(7, 13, 15), (7, 12, 14), (1, 12, 14), (7, 13, 14), (6, 13, 15), (6, 12, 15), (7, 12, 15), (6, 13, 14), (1, 13, 15), (1, 12, 15), (1, 13, 14), (6, 12, 14)}
	for i in [1,6,7,12,13,14,15]:
		for j in [1,6,7,12,13,14,15]:
			for k in [1,6,7,12,13,14,15]:
					if tuple([i,j]) in allowed_doubles and tuple([i,k]) in allowed_doubles and tuple([j,k]) in allowed_doubles:
						all_triples.add(tuple([i,j,k]))

	for i in [1,6,7,12,13,14,15]:
		for j in [1,6,7,12,13,14,15]:
			for k in [1,6,7,12,13,14,15]:
				for m in [1,6,7,12,13,14,15]:
					if tuple([i,j,k]) in allowed_triples and tuple([i,j,m]) in allowed_triples and tuple([i,k,m]) in allowed_triples and tuple([j,k,m]) in allowed_triples:
						all_quartets.add(tuple([i,j,k,m]))

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
		if max(diffs) == d:
			print(diffs)
			print(new_maj_vec)
			import pdb
			pdb.set_trace()
			break
		elif max(diffs) == d+1 and diffs.count(13) == d+1:
			print(diffs)
			nice_print([new_maj_vec])
			import pdb
			pdb.set_trace()
			counter_13 += 1
			all_singletons.add(diffs.index(d+1))
		elif max(diffs) == 13 and diffs.count(13) == 2:
			i = diffs.index(13)
			j = diffs.index(13, i+1)
			if i in [1,6,7,12,13,14,15] and j in [1,6,7,12,13,14,15] and tuple([i,j]) in all_doubles:
				all_doubles.remove(tuple([i,j]))
		elif max(diffs) == 13 and diffs.count(13) == 3:
			i = diffs.index(13)
			j = diffs.index(13, i+1)
			k = diffs.index(13, j+1)
			if tuple([i,j,k]) in all_triples:
				all_triples.remove(tuple([i,j,k]))
		elif max(diffs) == 13 and diffs.count(13) == 4:
			i = diffs.index(13)
			j = diffs.index(13, i+1)
			k = diffs.index(13, j+1)
			m = diffs.index(13, k+1)
			if tuple([i,j,k,m]) in all_triples:
				all_quartets.remove(tuple([i,j,k,m]))
	print("Number of max-13 diff vecotrs: {}".format(counter_13))
	print(all_singletons)
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


f = open("input_file1_d=14".format(random.choice([1,2,3,4,5])),"r+")
all_vecs = [elem.strip().replace(" ","")  for elem in f.readlines()]
#maj = "?" * 2*d
maj = find_maj([vec for vec in all_vecs]) 
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
