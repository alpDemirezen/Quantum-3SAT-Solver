import pycosat
from generate_instances import *

n = 5
k = 12

#soln_list = []

'''while len(soln_list) >= 4 or len(soln_list) == 0:
    soln_list = []
    line = create_CNF(n, k)
    for sol in pycosat.itersolve(line):
        soln_list.append(sol)

print(line)'''

line = create_CNF(n, k)
for sol in pycosat.itersolve(line):
    print(sol)
