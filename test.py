# --*-- conding:utf-8 --*--
# @Time : 10/23/24 PM1:21
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : test.py

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit_vqe import VQE
from qiskit.quantum_info import SparsePauliOp

# An example of use
if __name__ == '__main__':

    service = QiskitRuntimeService(
        channel='ibm_quantum',
        instance = 'a_instance',
        token = 'your_token_here'
    )

    hamiltonian_list = [("YZ", 0.3980), ("ZI", -0.3980), ("ZZ", -0.0113), ("XX", 0.1810)]

    hamiltonian = SparsePauliOp.from_list(hamiltonian_list) # Input data need a SparsePauliOp

    vqe = VQE(service=service, hamiltonian = hamiltonian)
    result = vqe.run_vqe()
    print("qiskit_vqe Result:", result)
