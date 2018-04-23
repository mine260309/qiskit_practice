#!/usr/bin/env python

from qiskit import QuantumProgram
import unittest


def shorU(obc, qr, cr, controlBit):
    obc.cx(qr[controlBit], qr[4])
    obc.cx(qr[controlBit], qr[5])
    obc.cx(qr[controlBit], qr[6])
    obc.cx(qr[controlBit], qr[7])

    obc.ccx(qr[controlBit], qr[6], qr[5])
    obc.ccx(qr[controlBit], qr[5], qr[6])
    obc.ccx(qr[controlBit], qr[6], qr[5])
    obc.ccx(qr[controlBit], qr[5], qr[4])
    obc.ccx(qr[controlBit], qr[4], qr[5])
    obc.ccx(qr[controlBit], qr[5], qr[4])
    obc.ccx(qr[controlBit], qr[7], qr[4])
    obc.ccx(qr[controlBit], qr[4], qr[7])
    obc.ccx(qr[controlBit], qr[7], qr[4])


def shorTest():
    # N=15 and a=7
    # Let's find period of f(x) = a^x mod N
    Circuit = 'shorTest'

    # Create the quantum program
    qp = QuantumProgram()

    # Creating registers
    n_qubits = 8
    qr = qp.create_quantum_register("qr", n_qubits)
    cr = qp.create_classical_register("cr", n_qubits)

    # We are going to find Q=2^q, where N^2 <= Q < 2*N^2
    # So the max Q is 450, needing 9 bits?
    
    # Shor algorithm with 4 qbits, where:
    # qr[0-3] are the bits for Q
    # qr[4-7] are the bits for U-gates
    obc = qp.create_circuit(Circuit, [qr], [cr])

    # Prepare bits
    obc.h(qr[0])
    obc.h(qr[1])
    obc.h(qr[2])
    obc.h(qr[3])

    # U0
    # U-a^2^0: multi 7*1
    # Refer to https://github.com/QISKit/ibmqx-user-guides/blob/master/rst/full-user-guide/004-Quantum_Algorithms/110-Shor's_algorithm.rst
    obc.x(qr[4])
    shorU(obc, qr, cr, 0)
    
    # U1
    shorU(obc, qr, cr, 1)
    shorU(obc, qr, cr, 1)

    # U2
    shorU(obc, qr, cr, 2)
    shorU(obc, qr, cr, 2)
    shorU(obc, qr, cr, 2)
    shorU(obc, qr, cr, 2)

    # U3
    shorU(obc, qr, cr, 3)
    shorU(obc, qr, cr, 3)
    shorU(obc, qr, cr, 3)
    shorU(obc, qr, cr, 3)
    shorU(obc, qr, cr, 3)
    shorU(obc, qr, cr, 3)
    shorU(obc, qr, cr, 3)
    shorU(obc, qr, cr, 3)

    # These are here for reference
#    # U-a^2^1: multi 7*7
#    obc.cx(qr[1], qr[5])
#    obc.cx(qr[1], qr[6])
#    obc.cx(qr[1], qr[7])
#    shorU(obc, qr, cr, 1)
#
#    # U-a^2^2: multi 7*4
#    obc.cx(qr[2], qr[5])
#    shorU(obc, qr, cr, 2)
#
#    # U-a^2^3: multi 7*13
#    obc.cx(qr[3], qr[4])
#    obc.cx(qr[3], qr[5])
#    obc.cx(qr[3], qr[7])
#    shorU(obc, qr, cr, 3)

    # Measure all gates
    for i in range(0, 8):
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
    #validate(results)


if __name__ == "__main__":
    shorTest()
