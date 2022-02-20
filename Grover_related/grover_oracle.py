import itertools
import pycosat
import matplotlib.pyplot as plt
import pandas as pd
from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit, Aer, BasicAer, IBMQ, execute
from qiskit.tools.visualization import plot_histogram
from qiskit.circuit.quantumcircuit import QuantumCircuit


def prepare_clause(circuit, clause):
    for element in clause:
        if element < 0:
            circuit.x(abs(element))
    return circuit


def or_operator(circuit, clause, counter):
    order_clause = [abs(x) for x in clause]
    for element in order_clause:
        circuit.x(element)
    circuit.mcx(order_clause, counter)
    circuit.x(counter)
    for element in order_clause:
        circuit.x(element)
    return circuit


def oracle(n, k, CNF):
    circuit = QuantumCircuit(n + k + 1)
    counter = n + 1
    for clause in CNF:
        prepare_clause(circuit, clause)
        or_operator(circuit, clause, counter)
        counter = counter + 1
        prepare_clause(circuit, clause)
    circuit.mcx(list(range(n + 1, n + k + 1)), 0)
    return circuit


def calculate_accuracy(sol_list, tup_list, n):
    counter = 0
    for sol in tup_list:
        if sol[0][0:n] in sol_list:
            counter += sol[1]
    return counter

def back_to_initial(outcome_reversed):
    back_list = []
    for i in range(1, len(outcome_reversed)):
        if outcome_reversed[i] == "0":
            back_list.append(0 - i)
        else:
            back_list.append(i)
    return back_list