from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()
print(session.evaluate(wlexpr("2 + 2")))
import random
import itertools
from copy import copy,deepcopy

d = 20
m = 40
chooser = [elem for elem in range(d)]


SUCCESS = False


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
	lst = list(itertools.product([0, 1], repeat=maj_vec.count("?")))

	for comb in lst:
		new_maj_vec = ""
		count = 0
		for i in range(len(maj_vec)):
			if maj_vec[i] == "?":
				new_maj_vec += str(comb[count])
				count += 1
			else:
				new_maj_vec += maj_vec[i]
		nice_print([new_maj_vec])
		diffs = [0 for vec in all_vecs]
		for i in range(len(new_maj_vec)):
			for j in range(len(all_vecs)):
				if all_vecs[j][i] != new_maj_vec[i]:
					diffs[j] += 1
		print(diffs)
		if max(diffs) < d:
			is_success = False
			break
	return is_success
				

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
			
			
def max_distance_from_reference(arr1, arr2):
	diffs = [0 for vec in arr2]
	for k in range(len(arr2)):
		granular_diffs = [0 for vec in arr1]
		for i in range(len(arr1[0])):
			for j in range(len(arr1)):
				if arr1[j][i] != arr2[k][i]:
					granular_diffs[j] += 1
		diffs[k] = max(granular_diffs)
	return diffs


def complete_vectors(vecs, diffs):
	added_length = 0
	new_vecs = deepcopy(vecs)
	for i in range(len(vecs)):
		added_length += d - diffs[i]
		for j in range(len(vecs)):
			if j != i:
				new_vecs[j] += "0" * (d - diffs[i])
			else:
				new_vecs[i] += "1" * (d - diffs[i])
	return new_vecs, added_length
		
		

while not SUCCESS:
	all_vecs = []
	all_vecs.append("0" * m)
	all_vecs.append("1" * d + "0" * (m - d))
	counter = 2

	while True:
		x_vars = []
		new_eqs = []
		#print("Every day I'm")
		random.shuffle(chooser)
		#print("Shuffling")
		diff_eqs = ["" for elem in all_vecs]
		for i in range(m):
			x_vars.append("x" + str(i))
			if i < d/2:
				new_eqs.append("x{} == 1".format(chooser[i])) 
			elif i < d:
				new_eqs.append("x{} == 0".format(chooser[i]))
			else:
				new_eqs.append("0 <= x{} <= 1".format(i))
			for j in range(len(diff_eqs)):
				diff_eqs[j] += "(x{} - {})^2".format(i, all_vecs[j][i])
				if i < m - 1:
					diff_eqs[j] += " + " 
				else:
					diff_eqs[j] += " == {}".format(d) 
				
		new_eqs += diff_eqs
		
		exec = "FindInstance[{" + ",".join(new_eqs) + "}, {" + ",".join(x_vars) + "}, Integers]"
		#print(exec)
		res = session.evaluate(wlexpr(exec))
		#print(res)
		if len(res) == 0:
			#print("FINAL VECTORS:")
			#print(all_vecs)
			print("FINAL COUNTER: {}".format(counter))
			#if counter > d - 1:
			if counter > 0:
				final_vecs = arrange_final_vecs(all_vecs)
				maj_vec = find_maj(final_vecs)
				SUCCESS = calculate_diffs(final_vecs, maj_vec)
				if SUCCESS:
					print("NO MAJ VECTOR IS A GOOD CENTER. IS THIS THE ONE?")
			break
		else:
			new_vec = ""
			for j in range(m):
				new_vec += str(res[0][j][1])
			all_vecs.append(new_vec)
			#print(new_vec)
			counter += 1
			#print(counter)




def attempt1():
	all_vecs = []
	all_vecs.append("0" * 12)
	all_vecs.append("1101 1011 0011".replace(" ",""))
	all_vecs.append("1101 0110 1011".replace(" ",""))
	all_vecs.append("1100 1101 1011".replace(" ",""))
	all_vecs.append("1011 1001 1110".replace(" ",""))
	all_vecs.append("1011 0110 1101".replace(" ",""))
	all_vecs.append("1010 1110 1101".replace(" ",""))
	all_vecs.append("0111 1001 1101".replace(" ",""))
	all_vecs.append("0111 0111 0110".replace(" ",""))
	all_vecs.append("0110 1111 0110".replace(" ",""))
	maj_vec = "?" * 12
	calculate_diffs(all_vecs, maj_vec)

def attempt2():
	all_vecs = []
	all_vecs.append("0" * 10 + "1" * 2)
	all_vecs.append("0" * 4 + "1" * 2 + "0" * 6)
	all_vecs.append("1" * 2 + "0" * 10)
	all_vecs.append("1010 1011 1010".replace(" ",""))
	all_vecs.append("1010 1100 0101".replace(" ",""))
	all_vecs.append("1001 0101 1110".replace(" ",""))
	all_vecs.append("1101 0011 0011".replace(" ",""))
	all_vecs.append("0111 1010 1101".replace(" ",""))
	all_vecs.append("0110 1100 0110".replace(" ",""))
	all_vecs.append("0101 0111 1001".replace(" ",""))
	original_length = len(all_vecs[0])
	diffs = max_distance_from_reference(all_vecs[:3], all_vecs[3:])
	updated_vecs, extra_length = complete_vectors(all_vecs[3:],diffs)
	final_vecs = deepcopy(all_vecs)
	for i in range(len(updated_vecs)):
		final_vecs[i+3] = updated_vecs[i]
	for i in range(3):
		final_vecs[i] += "0" * extra_length
	maj = find_maj(final_vecs)
	true_maj = "?" * original_length + maj[original_length:]
	res = calculate_diffs(final_vecs, true_maj)
	print(res)
	

attempt2()
