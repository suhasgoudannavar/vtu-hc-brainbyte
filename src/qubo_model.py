"""
QUBO (Quadratic Unconstrained Binary Optimization) Formulation for QRescue.
Maps the emergency resource allocation problem into a binary quadratic form
and Ising Hamiltonian for quantum circuit execution.
"""

from __future__ import annotations
from typing import List, Dict, Tuple, Any, Optional
import numpy as np

from qiskit.quantum_info import SparsePauliOp

from src.data_models import Incident, Resource
from src.response_time import calculate_incident_resource_response


class AllocationQUBO:
    """
    Constructs and manages the QUBO representation for disaster resource allocation.
    
    Variables:
        x[k] = x[i, r] in {0, 1}
        where k = i * n_resources + r
        
    Total qubits = n_incidents * n_resources
    """

    def __init__(
        self,
        incidents: List[Incident],
        resources: List[Resource],
        congestion_factor: float = 1.2,
        penalty_exclusivity: float = 80.0,
        penalty_mismatch: float = 120.0,
        penalty_unavailable: float = 150.0,
        weight_urgency: float = 25.0,
        weight_transit: float = 0.5,
    ):
        self.incidents = incidents
        self.resources = resources
        self.congestion_factor = congestion_factor
        
        self.n_inc = len(incidents)
        self.n_res = len(resources)
        self.num_qubits = self.n_inc * self.n_res
        
        self.penalty_excl = penalty_exclusivity
        self.penalty_mismatch = penalty_mismatch
        self.penalty_unavail = penalty_unavailable
        self.weight_urgency = weight_urgency
        self.weight_transit = weight_transit
        
        # Variable mapping: (i, r) -> index k, index k -> (i, r)
        self.var_to_index: Dict[Tuple[int, int], int] = {}
        self.index_to_var: Dict[int, Tuple[int, int]] = {}
        k = 0
        for i in range(self.n_inc):
            for r in range(self.n_res):
                self.var_to_index[(i, r)] = k
                self.index_to_var[k] = (i, r)
                k += 1
                
        self.Q_matrix: np.ndarray = np.zeros((self.num_qubits, self.num_qubits), dtype=float)
        self.constant_offset: float = 0.0
        self._build_qubo()

    def _build_qubo(self) -> None:
        """
        Builds the symmetric/upper-triangular QUBO matrix Q such that
        Cost(x) = x^T Q x + offset.
        """
        # 1. Linear terms: Transit cost minus priority reward
        for i, inc in enumerate(self.incidents):
            for r, res in enumerate(self.resources):
                k = self.var_to_index[(i, r)]
                resp = calculate_incident_resource_response(inc, res, self.congestion_factor)
                transit_time = resp["transit_time_min"]
                
                # Base cost: travel time penalty - urgency reward
                linear_cost = (self.weight_transit * transit_time) - (self.weight_urgency * (inc.urgency_score / 100.0))
                
                # Incompatibility penalty
                if res.resource_type not in inc.required_resource_types:
                    linear_cost += self.penalty_mismatch
                    
                # Unavailability penalty
                if not res.available:
                    linear_cost += self.penalty_unavail
                    
                self.Q_matrix[k, k] += linear_cost

        # 2. Quadratic penalty: Exclusivity (Resource r assigned to at most one incident)
        # Penalty: P_excl * (sum_i x_{i, r})^2 -> for each r, cross terms 2 * P_excl * x_{i, r} * x_{i', r}
        for r in range(self.n_res):
            for i1 in range(self.n_inc):
                k1 = self.var_to_index[(i1, r)]
                for i2 in range(i1 + 1, self.n_inc):
                    k2 = self.var_to_index[(i2, r)]
                    # Upper triangular storage: Q[k1, k2]
                    self.Q_matrix[k1, k2] += 2.0 * self.penalty_excl

        # 3. Quadratic penalty: Over-assignment to same incident
        # Encourage exactly or at most 1 resource per incident in simplified QUBO
        for i in range(self.n_inc):
            for r1 in range(self.n_res):
                k1 = self.var_to_index[(i, r1)]
                for r2 in range(r1 + 1, self.n_res):
                    k2 = self.var_to_index[(i, r2)]
                    self.Q_matrix[k1, k2] += 1.5 * self.penalty_excl

    def evaluate_bitstring(self, bitstring: str) -> float:
        """
        Evaluates the QUBO objective value for a binary string x in {0, 1}^N.
        """
        # Qiskit bitstring order is right-to-left (little endian), reverse to match variable index
        x = np.array([int(b) for b in reversed(bitstring)], dtype=float)
        val = float(x.T @ self.Q_matrix @ x) + self.constant_offset
        return val

    def to_ising_hamiltonian(self) -> Tuple[SparsePauliOp, float]:
        """
        Converts the QUBO problem into an Ising Hamiltonian H = sum_i h_i Z_i + sum_{i<j} J_ij Z_i Z_j + offset.
        Using substitution: x_k = (1 - Z_k) / 2.
        
        Returns:
            hamiltonian: SparsePauliOp
            offset: float
        """
        N = self.num_qubits
        h = np.zeros(N, dtype=float)
        J = np.zeros((N, N), dtype=float)
        offset = 0.0

        for i in range(N):
            # Linear Q_ii * x_i = Q_ii * (1 - Z_i)/2 = Q_ii/2 - (Q_ii/2) Z_i
            Q_ii = self.Q_matrix[i, i]
            offset += Q_ii / 2.0
            h[i] -= Q_ii / 2.0

            for j in range(i + 1, N):
                Q_ij = self.Q_matrix[i, j]
                if abs(Q_ij) < 1e-9:
                    continue
                # Q_ij * x_i * x_j = Q_ij * (1 - Z_i)(1 - Z_j) / 4
                #                  = Q_ij/4 - (Q_ij/4) Z_i - (Q_ij/4) Z_j + (Q_ij/4) Z_i Z_j
                offset += Q_ij / 4.0
                h[i] -= Q_ij / 4.0
                h[j] -= Q_ij / 4.0
                J[i, j] += Q_ij / 4.0

        pauli_list = []
        coeffs = []

        # Single Z terms
        for i in range(N):
            if abs(h[i]) > 1e-9:
                pauli_str = ["I"] * N
                pauli_str[i] = "Z"
                # Qiskit Pauli string order: qubit 0 is rightmost
                pauli_list.append("".join(reversed(pauli_str)))
                coeffs.append(h[i])

        # Two-qubit ZZ terms
        for i in range(N):
            for j in range(i + 1, N):
                if abs(J[i, j]) > 1e-9:
                    pauli_str = ["I"] * N
                    pauli_str[i] = "Z"
                    pauli_str[j] = "Z"
                    pauli_list.append("".join(reversed(pauli_str)))
                    coeffs.append(J[i, j])

        if not pauli_list:
            hamiltonian = SparsePauliOp.from_list([("I" * N, 0.0)])
        else:
            hamiltonian = SparsePauliOp.from_list(list(zip(pauli_list, coeffs)))

        return hamiltonian, offset

    def decode_solution(self, bitstring: str) -> Dict[str, Any]:
        """
        Decodes a binary bitstring into incident resource assignments.
        """
        x = [int(b) for b in reversed(bitstring)]
        assignments_map: Dict[str, List[str]] = {inc.id: [] for inc in self.incidents}
        
        for k, val in enumerate(x):
            if val == 1:
                i, r = self.index_to_var[k]
                assignments_map[self.incidents[i].id].append(self.resources[r].id)
                
        return assignments_map
