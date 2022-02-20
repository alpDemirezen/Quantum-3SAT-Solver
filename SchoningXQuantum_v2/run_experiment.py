from generate_instances import *
from Helpers import *
import generate_lines
from Quantum_alg import quantum_run, quantum_alg
from Schoning import schoning_run
from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
from qiskit.compiler import transpile
from matplotlib import pyplot as plt

'''n = 7
k = 18

line = create_CNF(n, k)'''

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

line_list = generate_lines.line_list
accuracy_list = generate_lines.accuracy_list
nk_list = generate_lines.nk_list
# print(len(get_solution_list(line)))

# for line, goal, nk in zip(line_list, accuracy_list, nk_list):
line = [[-1, 2, -6], [-2, -4, 6], [1, -2, -5], [-2, 5, -6], [2, -4, -6], [-3, -4, 6], [1, -4, -6], [1, -5, -6], [-1, 2, -5], [2, -5, -6], [-1, -4, 5], [-1, -3, 6], [-2, -4, 5], [-1, -5, 6], [4, -5, -6]]
print('hey')
total_it = 40
n = 6
k = 15
adim = 0
tuple_list = []
for step in range(3, 51):
    """accuracy = schoning_run(step, n, line, total_it)
    print("Steps ", step)
    print("Schöning Accuracy: ", accuracy)"""
    accuracy_q = quantum_run(step, n, line, total_it) / 1000
    print("Quantum accuracy: ", accuracy_q, 'step count', step)
    tuple_item = (accuracy_q, step)
    tuple_list.append(tuple_item)
    if accuracy_q >= 0.8179:
        print('hello', "Quantum accuracy: ", accuracy_q, 'step count', step)
        adim = step
        break
result = transpile(quantum_alg(n, line, adim)[1], optimization_level=2,
                   basis_gates=['id', 'rz', 'sx', 'x', 'cx', 'reset'])
print(result.depth())
print(result.count_ops())

x_axis = []
y_axis = []
for item in tuple_list:
    y_axis.append(item[0])
    x_axis.append(item[1])

print(x_axis, y_axis)
