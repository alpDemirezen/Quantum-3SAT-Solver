import generate_lines
from Quantum_alg import quantum_run, quantum_alg
from qiskit.compiler import transpile
import pickle

# You can change the variables from below
total_it = 40
n = generate_lines.n
k = generate_lines.k
successful_step = 0
shot_count = 1000
goal_accuracy = 0.75
min_step = 3
max_step = 4
accuracy_step_list = []
gate_list = ['id', 'rz', 'sx', 'x', 'cx', 'reset']

depth_file = open("depth_file", "w")
gates_file = open("gates_file", "w")
accuracy_file = open("accuracy_file", "w")
pickle_off = open('datafile.txt', "rb")
line = pickle.load(pickle_off)

for step in range(min_step, max_step):
    accuracy = quantum_run(step, n, line, total_it, shot_count) / shot_count
    accuracy_step_item = (accuracy, step)
    accuracy_step_list.append(accuracy_step_item)
    if accuracy >= goal_accuracy:
        successful_step = step
        break
result = transpile(quantum_alg(n, line, successful_step, shot_count)[1], optimization_level=2,
                   basis_gates=gate_list)

depth_file.write(str(result.depth()))
gates_file.write(str(result.count_ops()))
accuracy_file.write(str(accuracy_step_list))
