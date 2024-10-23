# --*-- conding:utf-8 --*--
# @Time : 10/23/24 PM1:19
# @Author : Yuqi Zhang
# @Email : yzhan135@kent.edu
# @File : vqe.py

import numpy as np
from qiskit.circuit.library import EfficientSU2
from qiskit.quantum_info import SparsePauliOp
from scipy.optimize import minimize
from qiskit_ibm_runtime import QiskitRuntimeService, Session, EstimatorV2 as Estimator
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


class VQE:
    def __init__(self, service, instance, token, hamiltonian_list, optimization_level=3, shots=1000):
        self.service = service
        self.instance = instance
        self.token = token
        self.shots = shots
        self.backend = self._select_backend()
        self.hamiltonian = SparsePauliOp.from_list(hamiltonian_list)
        self.ansatz = EfficientSU2(self.hamiltonian.num_qubits)
        self.optimization_level = optimization_level
        self.cost_history_dict = {"prev_vector": None, "iters": 0, "cost_history": []}

    def _select_backend(self):
        service = QiskitRuntimeService(channel='ibm_quantum', instance=self.instance, token=self.token)
        backend = service.least_busy(simulator=False, operational=True, min_num_qubits=100)
        return backend

    def _generate_pass_manager(self):
        target = self.backend.target
        pm = generate_preset_pass_manager(target=target, optimization_level=self.optimization_level)
        return pm

    def cost_func(self, params, ansatz_isa, hamiltonian_isa, estimator):
        pub = (ansatz_isa, [hamiltonian_isa], [params])
        result = estimator.run(pubs=[pub]).result()
        energy = result[0].data.evs[0]

        self.cost_history_dict["iters"] += 1
        self.cost_history_dict["prev_vector"] = params
        self.cost_history_dict["cost_history"].append(energy)
        print(f"Iters. done: {self.cost_history_dict['iters']} [Current cost: {energy}]")

        return energy

    def run_vqe(self):
        pm = self._generate_pass_manager()
        ansatz_isa = pm.run(self.ansatz)
        hamiltonian_isa = self.hamiltonian.apply_layout(layout=ansatz_isa.layout)

        x0 = np.random.random(self.ansatz.num_parameters)

        with Session(backend=self.backend) as session:
            estimator = Estimator(mode=session)
            estimator.options.default_shots = self.shots

            res = minimize(self.cost_func, x0, args=(ansatz_isa, hamiltonian_isa, estimator), method="cobyla")
        return res



