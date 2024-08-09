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
	counter_d1 = 0
	all_singletons = set([])
	for i in range(12):
		all_singletons.add(i)
	all_doubles = set([])
	all_triples = set([])
	all_quartets = set([])

	allowed_singles = {0, 1, 2, 4, 5, 6, 7, 8, 10, 11}
	allowed_doubles = {(5, 7), (0, 2), (5, 10), (0, 5), (1, 6), (2, 5), (0, 11), (6, 11), (6, 8), (4, 5), (4, 8), (8, 11), (0, 1), (0, 7), (2, 4), (1, 2), (10, 11), (2, 10), (1, 8), (6, 10), (4, 7), (4, 10), (5, 11), (8, 10), (1, 4), (0, 6), (1, 7), (2, 6), (7, 11), (7, 8)}
	allowed_triples = {(7, 13, 15), (7, 12, 14), (1, 12, 14), (7, 13, 14), (6, 13, 15), (6, 12, 15), (7, 12, 15), (6, 13, 14), (1, 13, 15), (1, 12, 15), (1, 13, 14), (6, 12, 14)}

	for i in allowed_singles:
		for j in allowed_singles:
			if i<j:
				all_doubles.add(tuple([i,j]))

	for i in allowed_singles:
		for j in allowed_singles:
			for k in allowed_singles:
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
		print(diffs)
		if max(diffs) < d:
			is_success = False
			print(diffs)
			nice_print([new_maj_vec])
			break
		elif max(diffs) == d+1 and diffs.count(d+1) == 1:
			#nice_print([new_maj_vec])
			#print(diffs)
			counter_d1 += 1
			i = diffs.index(d+1)
			if i in all_singletons:
				all_singletons.remove(i)
		elif max(diffs) == d+1 and diffs.count(d+1) == 2:
			i = diffs.index(d+1)
			j = diffs.index(d+1, i+1)
			if tuple([i,j]) in all_doubles:
				all_doubles.remove(tuple([i,j]))
		elif max(diffs) == d+1 and diffs.count(d+1) == 3:
			i = diffs.index(d+1)
			j = diffs.index(d+1, i+1)
			k = diffs.index(d+1, j+1)
			if tuple([i,j,k]) in all_triples:
				all_triples.remove(tuple([i,j,k]))
		elif max(diffs) == 13 and diffs.count(13) == 4:
			i = diffs.index(13)
			j = diffs.index(13, i+1)
			k = diffs.index(13, j+1)
			m = diffs.index(13, k+1)
			if tuple([i,j,k,m]) in all_triples:
				all_quartets.remove(tuple([i,j,k,m]))
	print("Number of max-(d+1) diff vectors: {}".format(counter_d1))
	print(all_triples)
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


f = open("input_file1".format(random.choice([1,2,3,4,5])),"r+")
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
