"""
Quantum Optimization Component for QRescue.
Implements a genuine Quantum Approximate Optimization Algorithm (QAOA) experiment
simulated with Qiskit and Qiskit Aer on a small disaster allocation instance.
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from scipy.optimize import minimize

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

from src.data_models import (
    Incident,
    Resource,
    Assignment,
    OptimizationResult,
)
from src.qubo_model import AllocationQUBO
from src.classical_optimizer import validate_assignments
from src.response_time import calculate_incident_resource_response


def build_qaoa_circuit(
    qubo: AllocationQUBO,
    gammas: List[float],
    betas: List[float],
) -> QuantumCircuit:
    """
    Constructs an explicit QAOA QuantumCircuit using Cost and Mixer Hamiltonians.
    
    Circuit Structure:
    1. Layer 0: Hadamard gates on all qubits (|0> -> |+>).
    2. For each QAOA layer p:
       a. Cost unitary exp(-i * gamma * H_C):
          - Linear terms: RZ(2 * gamma * h_i)
          - Pairwise ZZ terms: CX -> RZ(2 * gamma * J_ij) -> CX
       b. Mixer unitary exp(-i * beta * H_M):
          - Single qubit RX(2 * beta) on every qubit.
    3. Measure all qubits.
    """
    N = qubo.num_qubits
    p = len(gammas)
    
    qc = QuantumCircuit(N, N)
    
    # 1. State preparation: Uniform superposition
    qc.h(range(N))
    
    # Pre-extract Hamiltonian coefficients from QUBO
    # In Ising form: x_i = (1 - Z_i)/2
    # Linear and quadratic terms:
    h = np.zeros(N, dtype=float)
    J = np.zeros((N, N), dtype=float)
    for i in range(N):
        h[i] -= qubo.Q_matrix[i, i] / 2.0
        for j in range(i + 1, N):
            Q_ij = qubo.Q_matrix[i, j]
            if abs(Q_ij) > 1e-9:
                h[i] -= Q_ij / 4.0
                h[j] -= Q_ij / 4.0
                J[i, j] += Q_ij / 4.0

    # 2. QAOA Alternating Operators
    for layer in range(p):
        gamma = gammas[layer]
        beta = betas[layer]
        
        # --- Cost Hamiltonian Unitary U(C, gamma) ---
        # Single-qubit Z rotations
        for i in range(N):
            if abs(h[i]) > 1e-9:
                qc.rz(2.0 * gamma * h[i], i)
                
        # Two-qubit ZZ interactions
        for i in range(N):
            for j in range(i + 1, N):
                if abs(J[i, j]) > 1e-9:
                    qc.cx(i, j)
                    qc.rz(2.0 * gamma * J[i, j], j)
                    qc.cx(i, j)
                    
        # --- Mixer Hamiltonian Unitary U(M, beta) ---
        for i in range(N):
            qc.rx(2.0 * beta, i)
            
    # 3. Measurement
    qc.measure(range(N), range(N))
    return qc


def run_qaoa_optimizer(
    incidents: List[Incident],
    resources: List[Resource],
    congestion_factor: float = 1.2,
    p_layers: int = 1,
    shots: int = 1024,
    maxiter: int = 25,
    random_seed: int = 42,
    max_qubits: int = 12,
) -> OptimizationResult:
    """
    Executes QAOA on a small allocation instance.
    
    To maintain realistic simulation bounds on local CPU, if problem size exceeds
    max_qubits, selects the top critical incidents and nearest candidate resources.
    """
    start_time = time.perf_counter()
    
    if not incidents or not resources:
        return OptimizationResult(
            algorithm_name="Quantum Optimizer (QAOA - Qiskit Aer)",
            status="NO_SOLUTION",
            assignments=[],
            served_incident_ids=[],
            unserved_incident_ids=[i.id for i in incidents],
            total_weighted_response_time=0.0,
            total_operating_cost=0.0,
            objective_value=0.0,
            resource_utilization_rate=0.0,
            runtime_sec=0.0,
            constraint_violations=["No incidents or resources provided."],
            is_feasible=False,
        )

    # Sub-select for quantum simulation if instance is too large (> max_qubits)
    # E.g. top 3 incidents and 3 available resources = 9 qubits
    active_incidents = sorted(incidents, key=lambda x: x.urgency_score, reverse=True)
    avail_resources = [r for r in resources if r.available]
    if not avail_resources:
        avail_resources = resources[:3]
        
    # Scale problem to fit quantum budget
    sub_inc = active_incidents
    sub_res = avail_resources
    while (len(sub_inc) * len(sub_res)) > max_qubits:
        if len(sub_inc) >= len(sub_res) and len(sub_inc) > 2:
            sub_inc = sub_inc[:-1]
        elif len(sub_res) > 2:
            sub_res = sub_res[:-1]
        else:
            break
            
    qubo = AllocationQUBO(
        incidents=sub_inc,
        resources=sub_res,
        congestion_factor=congestion_factor,
        penalty_exclusivity=70.0,
        penalty_mismatch=100.0,
        penalty_unavailable=150.0,
        weight_urgency=20.0,
        weight_transit=0.4,
    )
    
    simulator = AerSimulator(seed_simulator=random_seed)
    
    # Objective evaluation function for classical parameter optimizer
    energy_history: List[float] = []
    
    def qaoa_energy_objective(params: np.ndarray) -> float:
        gammas = params[:p_layers]
        betas = params[p_layers:]
        
        qc = build_qaoa_circuit(qubo, gammas, betas)
        compiled_qc = transpile(qc, simulator, optimization_level=1)
        job = simulator.run(compiled_qc, shots=shots)
        result = job.result()
        counts = result.get_counts()
        
        # Calculate expected energy
        total_energy = 0.0
        for bitstring, count in counts.items():
            cost = qubo.evaluate_bitstring(bitstring)
            total_energy += cost * count
            
        expected_energy = total_energy / shots
        energy_history.append(float(expected_energy))
        return expected_energy

    # Initial parameter guess
    rng = np.random.default_rng(random_seed)
    init_params = rng.uniform(0.1, 0.8, size=2 * p_layers)
    
    # Classical optimization of quantum parameters via COBYLA
    opt_result = minimize(
        qaoa_energy_objective,
        init_params,
        method="COBYLA",
        options={"maxiter": maxiter, "rhobeg": 0.5},
    )
    
    opt_params = opt_result.x
    opt_gammas = opt_params[:p_layers]
    opt_betas = opt_params[p_layers:]
    
    # Run optimal circuit to sample solutions
    final_qc = build_qaoa_circuit(qubo, opt_gammas, opt_betas)
    compiled_final = transpile(final_qc, simulator, optimization_level=1)
    final_job = simulator.run(compiled_final, shots=shots)
    final_counts = final_job.result().get_counts()
    
    # Sort measured bitstrings by frequency and evaluate QUBO cost
    sorted_samples = sorted(final_counts.items(), key=lambda kv: kv[1], reverse=True)
    
    # Find candidate bitstring: balance highest probability and lowest energy
    best_bitstring = sorted_samples[0][0]
    best_cost = float("inf")
    candidate_ranking = []
    
    for b_str, count in sorted_samples[:10]:
        c = qubo.evaluate_bitstring(b_str)
        prob = count / shots
        candidate_ranking.append({
            "bitstring": b_str,
            "cost": round(c, 2),
            "probability": round(prob, 4),
            "shots": count,
        })
        if c < best_cost:
            best_cost = c
            best_bitstring = b_str

    # Decode bitstring into assignments
    decoded_map = qubo.decode_solution(best_bitstring)
    
    # Build complete Assignment objects for all incidents in the scenario
    resource_map = {r.id: r for r in resources}
    assignments: List[Assignment] = []
    served_ids: List[str] = []
    unserved_ids: List[str] = []
    assigned_resources: set = set()
    total_weighted_time = 0.0
    total_cost = 0.0
    
    for inc in incidents:
        assigned_rids = decoded_map.get(inc.id, [])
        assigned_rnames = [resource_map[r].name for r in assigned_rids if r in resource_map]
        
        max_transit_time = 0.0
        inc_cost = 0.0
        details = []
        
        for rid in assigned_rids:
            res = resource_map.get(rid)
            if res:
                assigned_resources.add(res.id)
                resp = calculate_incident_resource_response(inc, res, congestion_factor)
                t_time = resp["transit_time_min"]
                c_val = resp["estimated_operating_cost"]
                max_transit_time = max(max_transit_time, t_time)
                inc_cost += c_val
                details.append({
                    "resource_id": res.id,
                    "resource_name": res.name,
                    "type": res.resource_type,
                    "distance_km": resp["distance_km"],
                    "transit_time_min": t_time,
                    "cost": c_val,
                })
                
        assigned_types = [resource_map[r].resource_type for r in assigned_rids if r in resource_map]
        missing = [rt for rt in inc.required_resource_types if rt not in assigned_types]
        is_served = (len(missing) == 0 and len(inc.required_resource_types) > 0)
        
        if is_served:
            served_ids.append(inc.id)
            total_resp = max_transit_time + inc.estimated_service_duration
            total_weighted_time += total_resp * (inc.urgency_score / 100.0)
            total_cost += inc_cost
        else:
            unserved_ids.append(inc.id)
            
        assignments.append(
            Assignment(
                incident_id=inc.id,
                incident_name=inc.name,
                resource_ids=assigned_rids,
                resource_names=assigned_rnames,
                estimated_travel_time_min=round(max_transit_time, 2),
                total_response_time_min=round(max_transit_time + inc.estimated_service_duration, 2) if is_served else 0.0,
                operating_cost=round(inc_cost, 2),
                is_fully_served=is_served,
                missing_resource_types=missing,
                assignment_details=details,
            )
        )
        
    runtime = time.perf_counter() - start_time
    
    # Check constraints using the unified validator
    is_valid, violations = validate_assignments(incidents, resources, assignments)
    
    total_avail_count = sum(1 for r in resources if r.available)
    util_rate = round(len(assigned_resources) / max(1, total_avail_count), 4)
    
    unserved_penalty = sum(
        inc.urgency_score * 15.0 for inc in incidents if inc.id in unserved_ids
    )
    raw_objective = round(total_weighted_time + unserved_penalty + (total_cost * 0.05), 2)
    
    status_str = "FEASIBLE" if is_valid else "INFEASIBLE"
    
    metadata = {
        "num_qubits": qubo.num_qubits,
        "circuit_depth": compiled_final.depth(),
        "p_layers": p_layers,
        "shots": shots,
        "optimal_gammas": [round(float(g), 4) for g in opt_gammas],
        "optimal_betas": [round(float(b), 4) for b in opt_betas],
        "best_bitstring": best_bitstring,
        "candidate_ranking": candidate_ranking,
        "energy_history": [round(e, 2) for e in energy_history[:20]],
        "simulator": "Qiskit Aer (AerSimulator - CPU Statevector/Shot-based)",
        "scientific_note": (
            "Simulated on a classical CPU using Qiskit Aer. "
            "Runtimes include classical circuit simulation overhead and do NOT "
            "imply physical quantum hardware speedup or quantum advantage."
        ),
    }

    return OptimizationResult(
        algorithm_name="Quantum Optimizer (QAOA - Qiskit Aer)",
        status=status_str,
        assignments=assignments,
        served_incident_ids=served_ids,
        unserved_incident_ids=unserved_ids,
        total_weighted_response_time=round(total_weighted_time, 2),
        total_operating_cost=round(total_cost, 2),
        objective_value=raw_objective,
        resource_utilization_rate=util_rate,
        runtime_sec=round(runtime, 4),
        constraint_violations=violations,
        is_feasible=is_valid,
        metadata=metadata,
    )
