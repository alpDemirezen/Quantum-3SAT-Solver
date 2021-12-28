from qiskit.circuit.library.standard_gates import ZGate

CCCZ = ZGate().control(2)


def inversion_z(circuit, n):
    for i in range(1, n + 1):
        circuit.h(i)

    for i in range(1, n + 1):
        circuit.x(i)

    circuit.append(CCCZ, [1, 2, 3])

    for i in range(1, n + 1):
        circuit.x(i)

    for i in range(1, n + 1):
        circuit.h(i)
    return circuit
