"""
Unified Evaluation and Algorithm Benchmarking for QRescue.
Provides fair, side-by-side comparison across:
1. Greedy Baseline
2. Classical Optimizer (OR-Tools CP-SAT)
3. Quantum Optimizer (QAOA - Qiskit Aer)
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional
import pandas as pd
import numpy as np

from src.data_models import Incident, Resource, OptimizationResult
from src.classical_optimizer import run_greedy_baseline, run_ortools_optimizer
from src.quantum_optimizer import run_qaoa_optimizer


def calculate_percentage_improvement(baseline_val: float, test_val: float) -> Optional[float]:
    """
    Rigorously computes relative improvement percentage:
    ((baseline - test) / baseline) * 100.
    
    Returns None or 0.0 if baseline is non-positive to prevent false division-by-zero metrics.
    """
    if baseline_val <= 0:
        return 0.0
    improvement = ((baseline_val - test_val) / baseline_val) * 100.0
    return round(improvement, 2)


def run_full_comparison(
    incidents: List[Incident],
    resources: List[Resource],
    congestion_factor: float = 1.2,
    include_quantum: bool = True,
    qaoa_layers: int = 1,
    qaoa_shots: int = 512,
    qaoa_maxiter: int = 15,
    random_seed: int = 42,
) -> Dict[str, Any]:
    """
    Runs all algorithms on the exact same scenario inputs and returns structured comparison data.
    """
    results: Dict[str, OptimizationResult] = {}
    
    # 1. Greedy Baseline
    greedy_res = run_greedy_baseline(incidents, resources, congestion_factor)
    results["Greedy Baseline"] = greedy_res
    
    # 2. Classical OR-Tools
    classical_res = run_ortools_optimizer(
        incidents, resources, congestion_factor=congestion_factor
    )
    results["Classical (OR-Tools)"] = classical_res
    
    # 3. Quantum QAOA (optional / simulated)
    if include_quantum:
        quantum_res = run_qaoa_optimizer(
            incidents=incidents,
            resources=resources,
            congestion_factor=congestion_factor,
            p_layers=qaoa_layers,
            shots=qaoa_shots,
            maxiter=qaoa_maxiter,
            random_seed=random_seed,
        )
        results["Quantum (QAOA Aer)"] = quantum_res
        
    # Build comparison summary table
    summary_rows = []
    incident_map = {inc.id: inc for inc in incidents}
    
    baseline_obj = greedy_res.objective_value
    baseline_time = greedy_res.total_weighted_response_time
    
    for name, res in results.items():
        # Count served high-priority / critical incidents
        served_crit_high = sum(
            1 for i_id in res.served_incident_ids
            if incident_map.get(i_id) and incident_map[i_id].priority_category in ["Critical", "High"]
        )
        
        obj_imp = calculate_percentage_improvement(baseline_obj, res.objective_value)
        time_imp = calculate_percentage_improvement(baseline_time, res.total_weighted_response_time)
        
        summary_rows.append({
            "Algorithm": name,
            "Status": res.status,
            "Feasible": "Yes" if res.is_feasible else "No",
            "Served Incidents": len(res.served_incident_ids),
            "Unserved Incidents": len(res.unserved_incident_ids),
            "Critical/High Served": served_crit_high,
            "Weighted Resp Time (min)": res.total_weighted_response_time,
            "Operating Cost ($)": res.total_operating_cost,
            "Resource Utilization (%)": round(res.resource_utilization_rate * 100.0, 1),
            "Objective Value": res.objective_value,
            "Runtime (sec)": res.runtime_sec,
            "Objective Improvement vs Baseline (%)": f"{obj_imp}%" if obj_imp is not None else "N/A",
            "Constraint Violations": len(res.constraint_violations),
        })
        
    summary_df = pd.DataFrame(summary_rows)
    
    return {
        "results": results,
        "summary_df": summary_df,
        "baseline_algorithm": "Greedy Baseline",
        "incidents_count": len(incidents),
        "resources_count": len(resources),
        "congestion_factor": congestion_factor,
    }
