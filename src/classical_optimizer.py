"""
Classical Disaster Resource Optimization for QRescue.
Implements:
1. Strict constraint validation engine.
2. Greedy baseline allocation heuristic.
3. Mixed-Integer Linear Programming / CP-SAT optimizer using Google OR-Tools.
"""

from __future__ import annotations
import time
from typing import List, Dict, Any, Tuple, Optional
import numpy as np

from ortools.sat.python import cp_model

from src.data_models import (
    Incident,
    Resource,
    Assignment,
    OptimizationResult,
    ResourceType,
)
from src.response_time import (
    calculate_incident_resource_response,
    compute_cost_matrix,
)


def validate_assignments(
    incidents: List[Incident],
    resources: List[Resource],
    assignments: List[Assignment],
) -> Tuple[bool, List[str]]:
    """
    Independent constraint checker for any allocation solution.
    Checks:
    - Unavailable resources assigned.
    - Exclusivity: same resource assigned to multiple simultaneous incidents.
    - Capability / type mismatch.
    - Accurate service status (marking fully served only if all required types present).
    """
    violations: List[str] = []
    
    resource_map = {r.id: r for r in resources}
    incident_map = {i.id: i for i in incidents}
    
    # 1. Check exclusivity and availability
    assigned_resources_count: Dict[str, int] = {}
    
    for asgn in assignments:
        inc = incident_map.get(asgn.incident_id)
        if not inc:
            violations.append(f"Assignment references unknown incident {asgn.incident_id}.")
            continue
            
        assigned_types = []
        for rid in asgn.resource_ids:
            res = resource_map.get(rid)
            if not res:
                violations.append(f"Assignment references unknown resource {rid}.")
                continue
                
            # Check availability
            if not res.available:
                violations.append(
                    f"Resource '{res.name}' ({res.id}) is unavailable but was assigned to incident '{inc.name}' ({inc.id})."
                )
                
            # Track exclusivity count
            assigned_resources_count[rid] = assigned_resources_count.get(rid, 0) + 1
            if assigned_resources_count[rid] > 1:
                violations.append(
                    f"Exclusive Resource Conflict: '{res.name}' ({res.id}) was assigned to multiple incidents."
                )
                
            # Check type capability match
            if res.resource_type not in inc.required_resource_types:
                violations.append(
                    f"Capability Mismatch: Resource '{res.name}' of type '{res.resource_type}' "
                    f"does not match any required types {inc.required_resource_types} for incident '{inc.name}'."
                )
            assigned_types.append(res.resource_type)
            
        # Verify full fulfillment flag
        missing = [rt for rt in inc.required_resource_types if rt not in assigned_types]
        if asgn.is_fully_served and len(missing) > 0:
            violations.append(
                f"Fulfillment Inconsistency: Incident '{inc.name}' marked fully served but is missing {missing}."
            )
            
    is_valid = (len(violations) == 0)
    return is_valid, violations


def run_greedy_baseline(
    incidents: List[Incident],
    resources: List[Resource],
    congestion_factor: float = 1.2,
) -> OptimizationResult:
    """
    Greedy Allocation Baseline:
    1. Sort incidents by descending priority (urgency_score).
    2. For each required resource type, assign the nearest available, unassigned resource.
    """
    start_time = time.perf_counter()
    
    if not incidents or not resources:
        return OptimizationResult(
            algorithm_name="Greedy Baseline",
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

    # Sort incidents by priority (urgency_score) descending
    sorted_incidents = sorted(incidents, key=lambda x: x.urgency_score, reverse=True)
    
    available_resources = {r.id: r for r in resources if r.available}
    assigned_resources: set = set()
    
    assignments: List[Assignment] = []
    served_ids: List[str] = []
    unserved_ids: List[str] = []
    
    total_weighted_time = 0.0
    total_cost = 0.0
    
    for inc in sorted_incidents:
        assigned_rids: List[str] = []
        assigned_rnames: List[str] = []
        max_transit_time = 0.0
        inc_cost = 0.0
        details = []
        
        # Need to satisfy each required resource type
        req_types = list(inc.required_resource_types)
        for req_t in req_types:
            best_res = None
            best_time = float("inf")
            best_cost = 0.0
            best_dist = 0.0
            
            # Find nearest available resource of this type
            for r in available_resources.values():
                if r.id in assigned_resources:
                    continue
                if r.resource_type == req_t:
                    metrics = calculate_incident_resource_response(inc, r, congestion_factor)
                    if metrics["transit_time_min"] < best_time:
                        best_time = metrics["transit_time_min"]
                        best_cost = metrics["estimated_operating_cost"]
                        best_dist = metrics["distance_km"]
                        best_res = r
                        
            if best_res:
                assigned_rids.append(best_res.id)
                assigned_rnames.append(best_res.name)
                assigned_resources.add(best_res.id)
                max_transit_time = max(max_transit_time, best_time)
                inc_cost += best_cost
                details.append({
                    "resource_id": best_res.id,
                    "resource_name": best_res.name,
                    "type": req_t,
                    "distance_km": best_dist,
                    "transit_time_min": best_time,
                    "cost": best_cost,
                })
                
        # Check if fully served
        assigned_types = [available_resources[rid].resource_type for rid in assigned_rids]
        missing = [rt for rt in req_types if rt not in assigned_types]
        is_served = (len(missing) == 0 and len(req_types) > 0)
        
        if is_served:
            served_ids.append(inc.id)
            total_response_time = max_transit_time + inc.estimated_service_duration
            total_weighted_time += total_response_time * (inc.urgency_score / 100.0)
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
    
    # Calculate objective: response time + unserved penalties + cost factor
    unserved_penalty = sum(
        inc.urgency_score * 15.0 for inc in incidents if inc.id in unserved_ids
    )
    obj_val = round(total_weighted_time + unserved_penalty + (total_cost * 0.05), 2)
    
    total_avail_count = sum(1 for r in resources if r.available)
    util_rate = round(len(assigned_resources) / max(1, total_avail_count), 4)
    
    is_valid, violations = validate_assignments(incidents, resources, assignments)
    
    return OptimizationResult(
        algorithm_name="Greedy Baseline",
        status="FEASIBLE" if is_valid else "INFEASIBLE",
        assignments=assignments,
        served_incident_ids=served_ids,
        unserved_incident_ids=unserved_ids,
        total_weighted_response_time=round(total_weighted_time, 2),
        total_operating_cost=round(total_cost, 2),
        objective_value=obj_val,
        resource_utilization_rate=util_rate,
        runtime_sec=round(runtime, 4),
        constraint_violations=violations,
        is_feasible=is_valid,
        metadata={"assigned_resources": list(assigned_resources)},
    )


def run_ortools_optimizer(
    incidents: List[Incident],
    resources: List[Resource],
    congestion_factor: float = 1.2,
    weight_response_time: float = 1.0,
    weight_unserved_penalty: float = 15.0,
    weight_cost: float = 0.05,
    time_limit_sec: float = 10.0,
) -> OptimizationResult:
    """
    Classical Constraint Optimization using Google OR-Tools CP-SAT.
    
    Decision Variables:
    - x[i, r] in {0, 1}: Resource r assigned to Incident i
    - y[i] in {0, 1}: Incident i is fully served
    
    Constraints:
    1. Resource exclusivity: sum_i x[i, r] <= 1 for available resources.
    2. Unavailable resources: sum_i x[i, r] == 0 for unavailable resources.
    3. Type compatibility: x[i, r] == 0 if resource r's type is not required by incident i.
    4. Type fulfillment: for each required type t of incident i, sum_{r in R_t} x[i, r] >= y[i].
    5. Link fulfillment: sum_r x[i, r] >= len(required_types) * y[i].
    
    Objective:
    Minimize sum_{i,r} cost_ir * x[i, r] + sum_i penalty_i * (1 - y[i])
    """
    start_time = time.perf_counter()
    
    if not incidents or not resources:
        return OptimizationResult(
            algorithm_name="Classical Optimizer (OR-Tools)",
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

    model = cp_model.CpModel()
    n_inc = len(incidents)
    n_res = len(resources)
    
    # Precompute metrics
    cost_data: Dict[Tuple[int, int], Dict[str, float]] = {}
    for i, inc in enumerate(incidents):
        for r, res in enumerate(resources):
            cost_data[(i, r)] = calculate_incident_resource_response(inc, res, congestion_factor)
            
    # Variables
    x: Dict[Tuple[int, int], Any] = {}
    for i in range(n_inc):
        for r in range(n_res):
            x[(i, r)] = model.NewBoolVar(f"x_{i}_{r}")
            
    y: Dict[int, Any] = {}
    for i in range(n_inc):
        y[i] = model.NewBoolVar(f"y_{i}")
        
    # Constraint 1 & 2: Resource exclusivity & availability
    for r, res in enumerate(resources):
        if not res.available:
            for i in range(n_inc):
                model.Add(x[(i, r)] == 0)
        else:
            model.Add(sum(x[(i, r)] for i in range(n_inc)) <= 1)
            
    # Constraint 3: Type compatibility
    for i, inc in enumerate(incidents):
        for r, res in enumerate(resources):
            if res.resource_type not in inc.required_resource_types:
                model.Add(x[(i, r)] == 0)
                
    # Constraint 4: Type fulfillment for each required type
    for i, inc in enumerate(incidents):
        req_types = inc.required_resource_types
        if not req_types:
            model.Add(y[i] == 0)
            continue
            
        for req_t in req_types:
            matching_r = [r for r, res in enumerate(resources) if res.resource_type == req_t]
            if matching_r:
                model.Add(sum(x[(i, r)] for r in matching_r) >= y[i])
            else:
                model.Add(y[i] == 0)
                
        # Constraint 5: Link total assignments to y[i]
        model.Add(sum(x[(i, r)] for r in range(n_res)) >= len(req_types) * y[i])

    # Objective Function
    # Integer scaling factor for CP-SAT solver (scale by 100 for precision)
    SCALE = 100
    obj_terms = []
    
    for i, inc in enumerate(incidents):
        # Unserved penalty: weight_unserved_penalty * urgency_score * (1 - y[i])
        penalty_int = int(weight_unserved_penalty * inc.urgency_score * SCALE)
        obj_terms.append(penalty_int * (1 - y[i]))
        
        # Priority weight for response time
        p_weight = max(0.2, inc.urgency_score / 100.0)
        
        for r, res in enumerate(resources):
            travel_time = cost_data[(i, r)]["transit_time_min"]
            op_cost = cost_data[(i, r)]["estimated_operating_cost"]
            
            coeff = (weight_response_time * travel_time * p_weight) + (weight_cost * op_cost)
            coeff_int = int(coeff * SCALE)
            obj_terms.append(coeff_int * x[(i, r)])
            
    model.Minimize(sum(obj_terms))
    
    # Solve
    solver = cp_model.CpSolver()
    solver.parameters.max_time_in_seconds = time_limit_sec
    solver.parameters.num_search_workers = 4
    status_code = solver.Solve(model)
    
    runtime = time.perf_counter() - start_time
    
    if status_code not in (cp_model.OPTIMAL, cp_model.FEASIBLE):
        return OptimizationResult(
            algorithm_name="Classical Optimizer (OR-Tools)",
            status="INFEASIBLE" if status_code == cp_model.INFEASIBLE else "NO_SOLUTION",
            assignments=[],
            served_incident_ids=[],
            unserved_incident_ids=[i.id for i in incidents],
            total_weighted_response_time=0.0,
            total_operating_cost=0.0,
            objective_value=0.0,
            resource_utilization_rate=0.0,
            runtime_sec=round(runtime, 4),
            constraint_violations=["Solver found no feasible solution."],
            is_feasible=False,
        )

    # Extract Solution
    assignments: List[Assignment] = []
    served_ids: List[str] = []
    unserved_ids: List[str] = []
    assigned_resources: set = set()
    total_weighted_time = 0.0
    total_cost = 0.0
    
    for i, inc in enumerate(incidents):
        is_served = bool(solver.Value(y[i]))
        assigned_rids = []
        assigned_rnames = []
        max_transit_time = 0.0
        inc_cost = 0.0
        details = []
        
        for r, res in enumerate(resources):
            if solver.Value(x[(i, r)]) == 1:
                assigned_rids.append(res.id)
                assigned_rnames.append(res.name)
                assigned_resources.add(res.id)
                
                t_time = cost_data[(i, r)]["transit_time_min"]
                c_val = cost_data[(i, r)]["estimated_operating_cost"]
                max_transit_time = max(max_transit_time, t_time)
                inc_cost += c_val
                
                details.append({
                    "resource_id": res.id,
                    "resource_name": res.name,
                    "type": res.resource_type,
                    "distance_km": cost_data[(i, r)]["distance_km"],
                    "transit_time_min": t_time,
                    "cost": c_val,
                })
                
        assigned_types = [res.resource_type for res in resources if res.id in assigned_rids]
        missing = [rt for rt in inc.required_resource_types if rt not in assigned_types]
        
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
        
    total_avail_count = sum(1 for r in resources if r.available)
    util_rate = round(len(assigned_resources) / max(1, total_avail_count), 4)
    
    unserved_penalty = sum(
        inc.urgency_score * weight_unserved_penalty for inc in incidents if inc.id in unserved_ids
    )
    raw_objective = round(total_weighted_time + unserved_penalty + (total_cost * weight_cost), 2)
    
    is_valid, violations = validate_assignments(incidents, resources, assignments)
    
    status_str = "OPTIMAL" if status_code == cp_model.OPTIMAL else "FEASIBLE"
    if not is_valid:
        status_str = "INFEASIBLE"
        
    return OptimizationResult(
        algorithm_name="Classical Optimizer (OR-Tools)",
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
        metadata={
            "solver_wall_time_sec": solver.WallTime(),
            "solver_branches": solver.NumBranches(),
            "solver_conflicts": solver.NumConflicts(),
            "assigned_resources": list(assigned_resources),
        },
    )
