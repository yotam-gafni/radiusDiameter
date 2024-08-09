from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()
print(session.evaluate(wlexpr("2 + 2")))



def counterize(num):
	return bin(num)[2:].rjust(depth, "0")

def generate_equations(depth):
	new_eqs = []
	x_vars = []
	y_vars = []
	for i in range(2**depth):
		counter = counterize(i)
		new_x_str = "x" + counter
		new_y_str = "y" + counter
		x_vars.append(new_x_str)
		y_vars.append(new_y_str)
		new_eqs.append("{} >= 0".format(new_x_str))
		new_eqs.append("{} >= 0".format(new_y_str))
		if int(bin(i)[-1]) == 0:
			old_var_str = "x" + counter[:-1]
		elif int(bin(i)[-1]) == 1:
			old_var_str = "y" + counter[:-1]
		else:
			print("WHAT??")
		new_eqs.append("{} + {} == {}".format(new_x_str, new_y_str, old_var_str))
	modul = 2**depth
	new_eq = ""
	for j in range(2**depth):
		if (j // modul) % 2 == 0:
			new_eq += x_vars[j] 
		elif (j // modul) % 2 == 1:
			new_eq += y_vars[j] 
		if j != 2**depth - 1:
			new_eq += "+"
	new_eq += " == {}".format(n)
	new_eqs.append(new_eq)
	modul = modul / 2
	for i in range(1,depth+1):
		new_eq = ""
		for j in range(2**depth):
			if (j // modul) % 2 == 0:
				new_eq += y_vars[j] 
			elif (j // modul) % 2 == 1:
				new_eq += x_vars[j] 
			if j != 2**depth - 1:
				new_eq += "+"
		new_eq += " == {}".format(n)
		new_eqs.append(new_eq)
		modul = modul / 2

	new_vars = x_vars + y_vars
	return new_eqs, new_vars

			
		
n = 8

eqs = []
vars = []
eqs.append("x == {}".format(n))
eqs.append("y == m - {}".format(n))
vars.append("x")
vars.append("y")

for depth in range(1,n-1):
	new_eqs, new_vars = generate_equations(depth)
	print(new_eqs)
	eqs += new_eqs
	vars += new_vars
	
	# restricting, hopefully w.l.o.g., and the last equation is because otherwise we can turn these 1s to 0s and get a good 'center' outside the set
	#if depth == n-2:
	#	for j in range(depth - 1):
	#		new_eq = new_vars[0] + ">=" + new_vars[2**depth + 2**j]
	#		print(new_eq)
	#		eqs.append(new_eq)
	#	new_eq = new_vars[-1] + " == 0"
	#	eqs.append(new_eq)

exec = "FindInstance[{" + ",".join(eqs) + "}, {" + ",".join(vars) + "}, Integers]"
print(exec)
print(session.evaluate(wlexpr("With[{m=" + "{}".format(2*n - 2) + "}," + exec + "]")))

		
		
	

	
