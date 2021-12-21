import random
from math import pi

from qiskit import (Aer, ClassicalRegister, QuantumCircuit,
                    QuantumRegister, execute)

from helpers import back_to_initial, calculate_accuracy, get_solution_list


def clause_variables(clause):
    return [abs(int(c)) for c in clause]


def findZeroClauseN(mycircuit, clause):
    clauseToschoning = clause_variables(clause)
    for c in clause:
        if int(c) < 0:
            mycircuit.x(abs(int(c)))

    for i in clauseToschoning:
        mycircuit.x(i)

    mycircuit.mcx(clauseToschoning, [0])
    mycircuit.x([0])

    for i in clauseToschoning:
        mycircuit.x(i)

    for c in clause:
        if int(c) < 0:
            mycircuit.x(abs(int(c)))

    return mycircuit


def controller(fzc, mycircuit, qreg, variables):
    mycircuit.append(fzc, qargs=qreg)
    r = random.choice(variables)
    mycircuit.x(qreg[0])
    mycircuit.cx(qreg[0], qreg[r])
    mycircuit.barrier()
    mycircuit.reset(qreg[0])


def initialize_circuit(mycircuit, qreg):
    mycircuit.h(qreg[1:])
    #for i in range(1, len(qreg)):
    #    mycircuit.ry(2 * pi * random.uniform(0, 1), i)


def main_body(n, mycircuit, qreg, line, step):
    fzc_array = []
    for l in line:
        fzc_array.append(findZeroClauseN(QuantumCircuit(n + 1), l).to_gate())

    for i in range(step):
        r = random.randint(0, len(line) - 1)
        variables = clause_variables(line[r])
        controller(fzc_array[r], mycircuit, qreg, variables)


def quantum_run(step, n, line, total_it):
    accuracy = 0
    for it in range(total_it):
        accuracy += quantum_alg(n, line, step)
    accuracy /= total_it
    return accuracy


def quantum_alg(n, line, step):
    soln_list = get_solution_list(line)

    no_qubits = n + 1
    qreg = QuantumRegister(no_qubits)
    creg = ClassicalRegister(no_qubits)
    mycircuit = QuantumCircuit(qreg, creg)
    tuple_list = []

    initialize_circuit(mycircuit, qreg)

    main_body(n, mycircuit, qreg, line, step)

    mycircuit.measure(qreg, creg)
    job = execute(mycircuit, Aer.get_backend("qasm_simulator"), shots=1)
    counts = job.result().get_counts(mycircuit)

    # print the reverse of the outcome
    for outcome in counts:
        reverse_outcome = ""
        for i in outcome:
            reverse_outcome = i + reverse_outcome
        reverse_outcome = back_to_initial(reverse_outcome)
        tuple_list.append((reverse_outcome, counts[outcome]))
        # print(reverse_outcome, "is observed", counts[outcome], "times")
    accuracy = calculate_accuracy(soln_list, tuple_list)
    # print(mycircuit)
    return accuracy
