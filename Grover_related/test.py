from grover_oracle import *
from Inversion_related import *
from qiskit.compiler import transpile
import generated_lines

'''n = 3
k = 7
new_line = [[-1, -2, -3], [-1, -2, 3], [-1, 2, -3], [-1, 2, 3], [1, -2, -3], [1, -2, 3], [1, 2, -3]]
soln_list = []
for sol in pycosat.itersolve(new_line):
    soln_list.append(sol)

grover_circuit = QuantumCircuit(n + k + 1, n + k + 1)

for i in range(1, n + 1):
    grover_circuit.h(i)'''

iterations = 6
line_list = generated_lines.line_list
nk_list = generated_lines.nk_list
accuracy_list = []
# for new_line, nk in zip(line_list, nk_list):
n = 5
k = 16
soln_list = []
new_line = [[1, -2, -5], [-2, -3, 4], [-1, 4, -5], [-1, 2, -4], [-1, -3, 5], [1, -3, -4], [-2, -3, 4], [-1, -2, 4],
          [1, -2, -4], [2, -3, -4], [1, -3, -5], [3, -4, -5], [-2, 4, -5], [-2, -3, 5], [1, -3, -5], [-2, -4, 5]]
for sol in pycosat.itersolve(new_line):
    soln_list.append(sol)

grover_circuit = QuantumCircuit(n + k + 1, n + k + 1)

for i in range(1, n + 1):
    grover_circuit.h(i)
for i in range(iterations):
    grover_circuit += oracle(n, k, new_line)
    grover_circuit.z(0)
    grover_circuit += oracle(n, k, new_line).inverse()
    # grover_circuit.barrier()
    inversion_z(grover_circuit, n)
    # grover_circuit.barrier()
tuple_list = []

grover_circuit.measure([1, 2, 3], [1, 2, 3])

job = execute(grover_circuit, Aer.get_backend('qasm_simulator'), shots=10000)
# job = execute(mycircuit, backend= simulator_backend, shots=8192)
counts = job.result().get_counts(grover_circuit)
# print the reverse of the outcome
for outcome in counts:
    reverse_outcome = ''
    for i in outcome:
        reverse_outcome = i + reverse_outcome
    # print(reverse_outcome, "is observed", counts[outcome], "times")
    reverse_outcome = back_to_initial(reverse_outcome)
    tuple_list.append((reverse_outcome, counts[outcome]))
print("\n")
# print(tuple_list)
accuracy = calculate_accuracy(soln_list, tuple_list, n) / 10000
accuracy_list.append(accuracy)
result = transpile(grover_circuit, optimization_level=2, basis_gates=['id', 'rz', 'sx', 'x', 'cx', 'reset'])
print(result.depth())
print(result.count_ops())
print(accuracy_list)
