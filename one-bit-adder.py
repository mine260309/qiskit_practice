#!/usr/bin/env python

import sys
import unittest


class OneBitAdder(unittest.TestCase):
    results = {}

    def test_result(self):
        for r in self.results:
            self.assertTrue(len(r) == 4)
            a = int(r[3], 2)
            b = int(r[2], 2)
            x = int(r[0:2], 2)
            print("%d + %d = %d" % (a, b, x))
            self.assertEqual(x, a+b)


def validate(r):
    OneBitAdder.results = r
    unittest.main()


def oneBitAdder():
    from qiskit import QuantumProgram
    Circuit = 'oneBitAdderCircuit'

    # Create the quantum program
    qp = QuantumProgram()

    # Creating registers
    n_qubits = 4
    qr = qp.create_quantum_register("qr", n_qubits)
    cr = qp.create_classical_register("cr", n_qubits)

    # One-bit adder circuit, where:
    # qr[2] = qr[0] + qr[1]
    # qr[3] = carry
    obc = qp.create_circuit(Circuit, [qr], [cr])

    # Prepare bits to add
    obc.h(qr[0])
    obc.h(qr[1])

    # qr[2] = 1 when qr0/1 has only one 1;
    #       = 0 when qr0/1 are both 0 or 1;
    obc.cx(qr[0], qr[2])
    obc.cx(qr[1], qr[2])

    # qr[3] = 1 when qr0/1 are both 1;
    #       = 0 otherwise;
    obc.ccx(qr[0], qr[1], qr[3])

    # Measure
    for i in range(0, n_qubits):
        obc.measure(qr[i], cr[i])

    # Get qasm source
    source = qp.get_qasm(Circuit)
    print(source)

    # Compile and run
    backend = 'local_qasm_simulator'
    circuits = [Circuit]  # Group of circuits to execute

    qobj = qp.compile(circuits, backend)  # Compile your program

    result = qp.run(qobj, wait=2, timeout=240)
    print(result)

    results = result.get_counts(Circuit)
    print(results)
    validate(results)


if __name__ == "__main__":
    oneBitAdder()
