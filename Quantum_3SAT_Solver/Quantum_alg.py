import random

from qiskit import (Aer, ClassicalRegister, QuantumCircuit,
                    QuantumRegister, execute)

from Helpers import *


def clause_variables(clause):
    return [abs(int(c)) for c in clause]


def find_zero_clause(circuit, clause):
    clause_to_schoning = clause_variables(clause)
    for c in clause:
        if int(c) < 0:
            circuit.x(abs(int(c)))

    for i in clause_to_schoning:
        circuit.x(i)

    circuit.mcx(clause_to_schoning, [0])
    circuit.x([0])

    for i in clause_to_schoning:
        circuit.x(i)

    for c in clause:
        if int(c) < 0:
            circuit.x(abs(int(c)))

    return circuit


def controller(fzc, circuit, qreg, variables):
    circuit.append(fzc, qargs=qreg)
    r = random.choice(variables)
    circuit.x(qreg[0])
    circuit.cx(qreg[0], qreg[r])
    circuit.barrier()
    circuit.reset(qreg[0])


def initialize_circuit(circuit, qreg):
    circuit.h(qreg[1:])


def main_body(n, circuit, qreg, line, step):
    fzc_array = []
    for clause in line:
        fzc_array.append(find_zero_clause(QuantumCircuit(n + 1), clause).to_gate())
    r_list = []
    for i in range(step):
        r = random.randint(0, len(line) - 1)
        while r in r_list:
            r = random.randint(0, len(line) - 1)
        r_list.append(r)
        if len(r_list) == len(line):
            r_list = []
        variables = clause_variables(line[r])
        controller(fzc_array[r], circuit, qreg, variables)


def quantum_run(step, n, line, total_it, shot_count):
    accuracy = 0
    for it in range(total_it):
        accuracy += quantum_alg(n, line, step, shot_count)[0]
    accuracy /= total_it
    return accuracy


def quantum_outcome_gen(circuit, shot_count):
    tuple_list = []
    # preparing the outcome
    job = execute(circuit, Aer.get_backend("qasm_simulator"), shots=shot_count)
    counts = job.result().get_counts(circuit)
    # print the reverse of the outcome
    for outcome in counts:
        reverse_outcome = ""
        for i in outcome:
            reverse_outcome = i + reverse_outcome
        reverse_outcome = back_to_initial(reverse_outcome)
        tuple_list.append((reverse_outcome, counts[outcome]))

    return tuple_list


def quantum_alg(n, line, step, shot_count):
    # necessary initializations
    soln_list = get_solution_list(line)
    no_qubits = n + 1
    qreg = QuantumRegister(no_qubits)
    creg = ClassicalRegister(no_qubits)
    my_circuit = QuantumCircuit(qreg, creg)

    # circuit related operations
    initialize_circuit(my_circuit, qreg)
    main_body(n, my_circuit, qreg, line, step)
    my_circuit.measure(qreg, creg)

    tuple_list = quantum_outcome_gen(my_circuit, shot_count)
    accuracy = calculate_accuracy(soln_list, tuple_list)

    return accuracy, my_circuit
