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
