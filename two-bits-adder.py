#!/usr/bin/env python

from qiskit import QuantumProgram
import unittest


class TwoBitsAdder(unittest.TestCase):
    results = {}

    def test_result(self):
        for r in self.results:
            self.assertTrue(len(r) == 8)
            a = int(r[6:8], 2)
            b = int(r[4:6], 2)
            x = int(r[1:4], 2)
            print("%d + %d = %d" % (a, b, x))
            self.assertEqual(x, a+b)


def validate(r):
    TwoBitsAdder.results = r
    unittest.main()


def twoBitsAdder():
    Circuit = 'twoBitsAdderCircuit'

    # Create the quantum program
    qp = QuantumProgram()

    # Creating registers
    n_qubits = 8
    qr = qp.create_quantum_register("qr", n_qubits)
    cr = qp.create_classical_register("cr", n_qubits)

    # Two-bits adder circuit, where:
    # qr[0|1] and qr[2|3] are adders
    # qr[4-5] are the result
    # qr[6] is the carry_out
    # qr[7] is the temp reg
    obc = qp.create_circuit(Circuit, [qr], [cr])

    # Prepare bits to add
    obc.h(qr[0])
    obc.h(qr[1])
    obc.h(qr[2])
    obc.h(qr[3])

    # The low-bit result in qr[4]
    obc.cx(qr[0], qr[4])
    obc.cx(qr[2], qr[4])
    # The carry in temp reg
    obc.ccx(qr[0], qr[2], qr[7])

    # The high-bit result in qr[5]
    obc.cx(qr[1], qr[5])
    obc.cx(qr[3], qr[5])
    obc.cx(qr[7], qr[5])

    # The carry_out in qr[6]
    obc.ccx(qr[1], qr[3], qr[6])
    obc.ccx(qr[1], qr[7], qr[6])
    obc.ccx(qr[3], qr[7], qr[6])

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
    twoBitsAdder()
