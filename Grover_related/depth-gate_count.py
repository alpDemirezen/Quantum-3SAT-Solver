from qiskit.transpiler import PassManager
from test import *
from qiskit.compiler import transpile
from collections import defaultdict
from qiskit import transpile
from qiskit.transpiler.passes import Unroller
'''provider = IBMQ.load_account()
machine = provider.get_backend(f"ibmq_vigo")'''

result = transpile(grover_circuit,  basis_gates=['id', 'rz', 'sx', 'x', 'cx', 'reset'])
print(result.count_ops())
