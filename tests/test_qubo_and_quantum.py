"""
Unit tests for QUBO formulation, Ising Hamiltonian generation, and QAOA simulation.
"""

import pytest
import numpy as np
from src.data_models import Incident, Resource, DisasterCategory, ResourceType
from src.qubo_model import AllocationQUBO
from src.quantum_optimizer import build_qaoa_circuit, run_qaoa_optimizer


def test_qubo_construction():
    incidents = [
        Incident("I1", "Fire 1", DisasterCategory.FIRE.value, 37.7, -122.4, 5, 4,
                 required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value]),
        Incident("I2", "Medical 1", DisasterCategory.MEDICAL_EMERGENCY.value, 37.75, -122.42, 2, 3,
                 required_resource_types=[ResourceType.AMBULANCE.value]),
    ]
    resources = [
        Resource("R1", "Fire Engine", ResourceType.FIRE_RESPONSE_TEAM.value, 37.71, -122.41),
        Resource("R2", "Ambulance", ResourceType.AMBULANCE.value, 37.76, -122.43),
    ]
    
    # 2 incidents x 2 resources = 4 decision variables / qubits
    qubo = AllocationQUBO(incidents, resources)
    assert qubo.num_qubits == 4
    assert qubo.Q_matrix.shape == (4, 4)

    # Test bitstring evaluation
    val_all_zeros = qubo.evaluate_bitstring("0000")
    val_valid_assignment = qubo.evaluate_bitstring("1001")  # I1->R1 and I2->R2
    assert isinstance(val_all_zeros, float)
    assert isinstance(val_valid_assignment, float)


def test_qubo_to_ising_hamiltonian():
    incidents = [
        Incident("I1", "Fire", DisasterCategory.FIRE.value, 37.7, -122.4, 5, 4,
                 required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value]),
    ]
    resources = [
        Resource("R1", "Engine", ResourceType.FIRE_RESPONSE_TEAM.value, 37.7, -122.4),
        Resource("R2", "Ambulance", ResourceType.AMBULANCE.value, 37.7, -122.4),
    ]
    qubo = AllocationQUBO(incidents, resources)
    hamiltonian, offset = qubo.to_ising_hamiltonian()
    
    assert hamiltonian.num_qubits == 2
    assert len(hamiltonian.paulis) > 0
    assert isinstance(offset, float)


def test_build_qaoa_circuit():
    incidents = [
        Incident("I1", "Fire", DisasterCategory.FIRE.value, 37.7, -122.4, 5, 4,
                 required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value]),
    ]
    resources = [
        Resource("R1", "Engine", ResourceType.FIRE_RESPONSE_TEAM.value, 37.7, -122.4),
    ]
    qubo = AllocationQUBO(incidents, resources)
    
    qc = build_qaoa_circuit(qubo, gammas=[0.5], betas=[0.3])
    assert qc.num_qubits == 1
    assert qc.num_clbits == 1


def test_qaoa_optimizer_execution():
    incidents = [
        Incident("I1", "Fire", DisasterCategory.FIRE.value, 37.7, -122.4, 5, 4,
                 required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value]),
        Incident("I2", "Accident", DisasterCategory.ROAD_ACCIDENT.value, 37.75, -122.45, 3, 3,
                 required_resource_types=[ResourceType.AMBULANCE.value]),
    ]
    resources = [
        Resource("R1", "Engine", ResourceType.FIRE_RESPONSE_TEAM.value, 37.71, -122.41),
        Resource("R2", "Ambulance", ResourceType.AMBULANCE.value, 37.74, -122.44),
    ]
    
    result = run_qaoa_optimizer(
        incidents=incidents,
        resources=resources,
        p_layers=1,
        shots=256,
        maxiter=5,
        random_seed=42,
    )
    assert result.algorithm_name == "Quantum Optimizer (QAOA - Qiskit Aer)"
    assert result.status in ["FEASIBLE", "INFEASIBLE"]
    assert len(result.assignments) == 2
    assert "num_qubits" in result.metadata
    assert "simulator" in result.metadata
