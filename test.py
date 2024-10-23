# --*-- conding:utf-8 --*--
# @Time : 10/23/24 PM1:21
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : test.py

from qiskit_ibm_runtime import QiskitRuntimeService, Session, EstimatorV2 as Estimator
from qiskit_vqe import VQE

# An example of use
if __name__ == '__main__':
    service = QiskitRuntimeService()
    instance = 'a_instance'
    token = 'your_token_here'

    hamiltonian_list = [("YZ", 0.3980), ("ZI", -0.3980), ("ZZ", -0.0113), ("XX", 0.1810)]

    vqe = VQE(service=service, instance=instance, token=token, hamiltonian_list=hamiltonian_list)
    result = vqe.run_vqe()
    print("qiskit_vqe Result:", result)
