from test import *
from collections import defaultdict
from qiskit import transpile
from qiskit.transpiler.passes import Unroller
print(grover_circuit.count_ops())