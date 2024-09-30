from qiskit import QuantumCircuit
from numpy.linalg import svd, norm
from qclib.unitary import unitary
from math import floor, log2

"""
Implements the state preparation defined at https://arxiv.org/abs/1003.5760.
"""

class Plesch():

    def build(statevector):
        n = int(log2(len(statevector)))
        odd = n % 2
        n_half = floor(n/2)
        n_list = list(range(n))
        first_half = n_list[:n_half]
        second_half = n_list[n_half:]

        statevector.shape = (int(2 ** (n // 2)), int(2 ** (n // 2 + odd)))
        matrix_phase_3, coeffs, matrix_phase_4 = svd(statevector)
        coeffs = coeffs / norm(coeffs)

        qc = QuantumCircuit(n)

        qc.initialize(coeffs, first_half)
        qc.barrier()

        for i in first_half:
            qc.cx(i, i+n_half)
        qc.barrier()

        gate_phase_3 = unitary(matrix_phase_3)
        qc.append(gate_phase_3, first_half if odd else second_half)

        gate_phase_4 = unitary(matrix_phase_4.T)
        qc.append(gate_phase_4, second_half if odd else first_half)

        return qc