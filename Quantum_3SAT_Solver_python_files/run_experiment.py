import generate_lines
from Quantum_alg import quantum_run, quantum_alg
from qiskit.compiler import transpile
import pickle
import argparse


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("CNF", type=str,
                        choices=["datafile3_7.txt", "datafile3_10.txt", "datafile4_10.txt", "datafile4_15.txt",
                                 "datafile5_12.txt", "datafile5_16.txt", "datafile6_15.txt", "datafile6_18.txt",
                                 "datafile7_15.txt", "datafile7_18.txt"],
                        help="Input files to recreate the results")
    parser.add_argument("n", type=int,
                        help="Number of variables.")
    parser.add_argument("k", type=int,
                        help="Number of clauses.")
    parser.add_argument("-shot_count", type=int, default=1000,
                        help="Number of shots for the simulator.")
    parser.add_argument("-min_step", type=int, default=3,
                        help="Number of minimum steps.")
    parser.add_argument("-max_step", type=int, default=51,
                        help="Number of maximum steps.")
    parser.add_argument("goal_accuracy", type=float,
                        help="The accuracy to reach.")
    parser.add_argument("-total_iteration", type=int, default=40,
                        help="Number of iterations to run the quantum algorithm to acquire accuracy.")

    args = parser.parse_args()


total_it = args.total_iteration
successful_step = 0
min_step = args.min_step
max_step = args.max_step
n = args.n
k = args.k
shot_count = args.shot_count
goal_accuracy = args.goal_accuracy
accuracy_step_list = []
gate_list = ['id', 'rz', 'sx', 'x', 'cx', 'reset']

depth_file = open("depth_file", "w")
gates_file = open("gates_file", "w")
accuracy_file = open("accuracy_file", "w")
pickle_off = open('datafile3_7.txt', "rb")
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

