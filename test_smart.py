from wolframclient.evaluation import WolframLanguageSession
from wolframclient.language import wl, wlexpr
session = WolframLanguageSession()
import time
import itertools

d = 20
m = 38

def det_new_vec(all_vecs):
        x_vars = []
        new_eqs = []
        diff_eqs = ["" for elem in all_vecs]
        for i in range(m):
                x_vars.append("x" + str(i))
                new_eqs.append("0 <= x{} <= 1".format(i))
                column_sum = 0
                num_diffs = len(diff_eqs)
                for j in range(num_diffs):
                        column_sum += int(all_vecs[j][i])
                        diff_eqs[j] += "(x{} - {})^2".format(i, all_vecs[j][i])
                        if i < m - 1:
                                diff_eqs[j] += " + "
                        else:
                                diff_eqs[j] += " == {}".format(18)

        new_eqs += diff_eqs


        exec = "FindInstance[{" + ",".join(new_eqs) + "}, {" + ",".join(x_vars) + "}, Integers]"
        return exec
f = open("input_file","r+")
all_vecs = [elem.strip().replace(" ","") for elem in f.readlines()]

all_locs_x = [i for i in range(10)]
for x in range(1,10):
	y = 10 - x
	for comb_x in itertools.combinations(all_locs_x,x):
		



exec = det_new_vec(all_vecs)
res = session.evaluate(wlexpr(exec))
print(res)
