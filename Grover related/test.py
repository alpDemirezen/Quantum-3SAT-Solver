from grover_oracle import *
from Inversion_related import *

n = 3
k = 7
new_line = [[-1, -2, -3], [-1, -2, 3], [-1, 2, -3], [-1, 2, 3], [1, -2, -3], [1, -2, 3], [1, 2, -3]]
for sol in pycosat.itersolve(new_line):
    print(sol)
[-1, -2, -3]
grover_circuit = QuantumCircuit(n + k + 1, n + k + 1)

for i in range(1, n + 1):
    grover_circuit.h(i)

iterations = 2

for i in range(iterations):
    grover_circuit += oracle(n, k, new_line)
    grover_circuit.z(0)
    grover_circuit += oracle(n, k, new_line).inverse()
    # grover_circuit.barrier()
    inversion_z(grover_circuit, n)
    # grover_circuit.barrier()

grover_circuit.measure([1, 2, 3], [1, 2, 3])

job = execute(grover_circuit, Aer.get_backend('qasm_simulator'), shots=10000)
# job = execute(mycircuit, backend= simulator_backend, shots=8192)
counts = job.result().get_counts(grover_circuit)
# print the reverse of the outcome
for outcome in counts:
    reverse_outcome = ''
    for i in outcome:
        reverse_outcome = i + reverse_outcome
    print(reverse_outcome, "is observed", counts[outcome], "times")
print("\n")
