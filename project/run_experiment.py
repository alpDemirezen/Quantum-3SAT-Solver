from generate_instance import *
from helpers import *
from quantum_alg import quantum_run
from schoning import schoning_run

n = 3
k =  7
line = create_CNF(n, k)
'''
line = [
    [-1, 4, -5],
    [-1, -3, 5],
    [-3, -4, 5],
    [1, -2, -3],
    [-1, 2, -3],
    [-1, 2, -4],
    [-2, 3, -4],
    [-2, 3, -5],
    [-2, 3, -5],
    [-1, -3, 5],
    [2, -4, -5],
    [1, -2, -5],
    [-3, -4, 5],
    [1, -2, -4],
    [-2, -3, 5],
    [-3, 4, -5],
    [-2, 4, -5],
    [2, -4, -5],
    [1, -4, -5],
    [-2, 3, -5],
    [2, -4, -5],
    [-1, -2, 4],
    [2, -3, -5],
    [-1, 3, -4],
    [1, -2, -3],
]
'''

print(line)
print(len(get_solution_list(line)))

total_it = 1000

for step in range(0, 10):
    accuracy = schoning_run(step, n, line, total_it)
    print("Steps ", step)
    print("Schöning Accuracy: ", accuracy)
    accuracy_q = quantum_run(step, n, line, total_it)
    print("Quantum accuracy: ", accuracy_q)