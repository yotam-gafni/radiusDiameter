from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()
print(session.evaluate(wlexpr("2 + 2")))
import random
import itertools
from copy import copy,deepcopy
import pickle
from datetime import datetime
import time

d = 16
m = 2*d

# try the largest odd number that gives a better than existing ratio
#N = int(1.4 * d -0.01)
N = 2*d - 1
#if N % 2 == 0:
#	N = N - 1
#N = 2*d

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
	lst = itertools.product([0, 1], repeat=maj_vec.count("?"))
	
	min_avg = d

	counter = 0
	s = time.time()
	for comb in lst:
		counter += 1
		count = 0
		if counter % (100 * 1000) == 0:
			print(counter)
			e = time.time()
			print(e - s)
			s = time.time()
		new_maj_vec = ""
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
		#print(diffs)
		min_avg = min(min_avg, sum(diffs) / len(diffs))
		if max(diffs) < d:
			is_success = False
			print("Found a good center, moving on")
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
		

def random_new_vec(all_vecs, chooser):
	x_vars = []
	new_eqs = []
	random.shuffle(chooser)
	print(chooser)
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
	if len(res) == 0:
		return None
	else:
		new_vec = ""
		for j in range(m):
			new_vec += str(res[0][j][1])
		return new_vec

def calc_opt_coeffs(all_vecs):
	coeffs = []
	decisions = []

	tot = len(all_vecs) 

	for i in range(m):
		column_sum = 0
		for j in range(len(all_vecs)):
			column_sum += int(all_vecs[j][i])
		if column_sum >= tot / 2:
			decisions.append(0)
			#coeffs.append(column_sum - tot/2)
			coeffs.append(1)
		else:
			decisions.append(1)
			#coeffs.append(tot/2 - column_sum)
			coeffs.append(1)
	return decisions, coeffs

def det_new_vec(all_vecs, dist):
	x_vars = []
	new_eqs = []
	new_eqs2 = []
	diff_eqs = ["" for elem in all_vecs]
	diff_eqs2 = ["" for elem in all_vecs]
	opt_goal = ""
	decisions, coeffs = calc_opt_coeffs(all_vecs)
	for i in range(m):
		x_vars.append("x" + str(i))
		new_eqs.append("0 <= x{} <= 1".format(i))
		new_eqs2.append("0 <= x{} <= 1".format(i))
		for j in range(len(diff_eqs)):
			diff_eqs[j] += "(x{} - {})^2".format(i, all_vecs[j][i])
			diff_eqs2[j] += "(x{} - {})^2".format(i, all_vecs[j][i])
			if i < m - 1:
				diff_eqs[j] += " + " 
				diff_eqs2[j] += " + " 
			else:
				diff_eqs[j] += " == {}".format(dist) 
				diff_eqs2[j] += " < {}".format(dist) 
		if decisions[i] == 0:
			opt_goal += "{}*(x{})^2".format(coeffs[i],i)
		else:
			opt_goal += "{}*(x{} - 1)^2".format(coeffs[i],i)
		if i < m - 1:
			opt_goal += " + "
		else:
			opt_goal += ","
			
	new_eqs += diff_eqs
	new_eqs2 += diff_eqs2

	
	exec = "FindInstance[{" + ",".join(new_eqs) + "}, {" + ",".join(x_vars) + "}, Integers]"
	#execLess = "FindInstance[{" + ",".join(new_eqs2) + "}, {" + ",".join(x_vars) + "}, Integers]"
	#print(exec)
	exec2 = "NMinimize[{" + opt_goal + ",".join(new_eqs) + "}, {" + ",".join(x_vars) + "} \u2208 Integers]"
	#print(exec)
	#resLess = session.evaluate(wlexpr(execLess))
	#if len(resLess) == 0 and len(all_vecs) < 2 * d:
	#	import pdb
	#	pdb.set_trace()
	res = session.evaluate(wlexpr(exec))
	#print(res)
	if len(res) == 0:
		return None
	else:
		if dist == d:
			#print(exec2)
			res2 = session.evaluate(wlexpr(exec2))
			new_vec = ""
			for j in range(m):
				new_vec += str(res2[1][j][1])
			return new_vec
		else:
			return res



while not SUCCESS:
	all_vecs = []
	all_vecs.append("0" * m)
	all_vecs.append("1" * d + "0" * (m - d))
	counter = 2

	while True:
		if counter <= 4:
			new_vec = random_new_vec(all_vecs, chooser)
		else:
			new_vec = det_new_vec(all_vecs, d)
		
		if new_vec is None or len(all_vecs) >= N:
			if  len(all_vecs) >= d-2:
				print(counter)
				counter = 2
				#final_vecs = arrange_final_vecs(all_vecs)
				final_vecs = all_vecs
				nice_print(final_vecs)
				maj_vec = find_maj(final_vecs)
				print("MAJ_VEC: {}".format(maj_vec))
				#if "?" in maj_vec:
				#	print("INCONCLUSIVE MAJ VEC, MOVING ON")
				#	break
				SUCCESS, min_avg = calculate_diffs(final_vecs, maj_vec)
				#SUCCESS = True
				#min_avg = d-1
				if SUCCESS:
					print("NO MAJ VECTOR IS A GOOD CENTER. IS THIS THE ONE? MIN AVG DISTANCE: {} WITH d={}".format(min_avg,d))
					pickle.dump(final_vecs,open("d={},m={},time={}".format(d,m,str(datetime.now())),"wb+"))
					#res = det_new_vec(final_vecs, d - 1)
					#if res is None:
					#	import pdb
					#	pdb.set_trace()
					#else:
					#	print(res)
					#	print("Found a center {} away from all nodes".format(d-1))
					#	SUCCESS = False
					if min_avg > d-2:
						#print("BIG SUCCESS. But moving no, maybe it's a Hadamard...")
						print("Interesting...")
						SUCC, avg = calculate_diffs(all_vecs, "?" * m)
						if SUCC:
							print("THIS WORKS, TRY TO COMBINE")
							SUCCESS = False
						#for j in range(N-1,d-2,-1):
						#	print("Trying to see if the first {} vectors are an example".format(j))
						#	maj = find_maj(all_vecs[:j])
						#	SUCC, avg = calculate_diffs(all_vecs[:j], maj)
						#	if SUCC and avg > d - 1:
						#		print("{} vectors are enough, with avg: {}".format(j,avg))
						#		import pdb
						#		pdb.set_trace()
						#	else:
						#		SUCCESS = False
						#		break
					else:
						print("Maybe not too promising...")
						SUCCESS = False
				break
			else:
				counter = 2
				break
				
		else:
			all_vecs.append(new_vec)
			counter += 1
			print(counter)




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
	
def attempt3():
	all_vecs = []
	all_vecs.append("0" * m)
	all_vecs.append("1" * d + "0" * (m-d))
	



attempt3()
