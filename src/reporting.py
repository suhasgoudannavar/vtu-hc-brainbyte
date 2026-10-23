"""
Experiment Reporting and Data Export Module for QRescue.
Generates comprehensive JSON, CSV, and Markdown audit reports
for reproducible disaster response optimization experiments.
"""

from __future__ import annotations
import json
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import pandas as pd

from src.data_models import Scenario, Incident, Resource, OptimizationResult


def create_experiment_payload(
    scenario: Scenario,
    results: Dict[str, OptimizationResult],
    selected_algorithm: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Assembles a complete, self-contained experiment payload for export and audit.
    """
    timestamp = datetime.now().isoformat()
    exp_id = f"QRESCUE-EXP-{int(time.time())}"
    
    # Incident summary data
    incidents_data = [inc.to_dict() for inc in scenario.incidents]
    resources_data = [res.to_dict() for res in scenario.resources]
    
    # Results dictionary
    results_data = {
        name: res.to_dict() for name, res in results.items()
    }
    
    payload = {
        "experiment_id": exp_id,
        "timestamp": timestamp,
        "scenario": {
            "id": scenario.id,
            "name": scenario.name,
            "description": scenario.description,
            "scenario_type": scenario.scenario_type,
            "road_congestion_factor": scenario.road_congestion_factor,
            "weather_impact": scenario.weather_impact,
            "random_seed": scenario.random_seed,
        },
        "incidents": incidents_data,
        "resources": resources_data,
        "selected_algorithm": selected_algorithm or list(results.keys())[0] if results else None,
        "algorithms": results_data,
        "scientific_assumptions": [
            "Coordinates and street topologies are synthetic simulations.",
            "Straight-line distances are modified by a 1.35x road curvature factor.",
            "Vehicle speeds are nominal averages adjusted by congestion and access difficulty.",
            "Quantum optimization is simulated classically via Qiskit Aer.",
            "Runtimes measured on simulator reflect classical simulation cost, not physical QPU speed.",
            "This prototype is an educational and research simulation, not a certified emergency dispatch system.",
        ],
    }
    return payload


def export_experiment_json(payload: Dict[str, Any], indent: int = 2) -> str:
    """Exports full experiment data to a formatted JSON string."""
    return json.dumps(payload, indent=indent)


def export_experiment_csv_bundle(payload: Dict[str, Any]) -> Dict[str, str]:
    """
    Exports individual tables as CSV strings:
    - incidents.csv
    - resources.csv
    - assignments.csv
    - summary.csv
    """
    csv_dict: Dict[str, str] = {}
    
    # 1. Incidents CSV
    if payload.get("incidents"):
        df_inc = pd.DataFrame(payload["incidents"])
        csv_dict["incidents.csv"] = df_inc.to_csv(index=False)
        
    # 2. Resources CSV
    if payload.get("resources"):
        df_res = pd.DataFrame(payload["resources"])
        csv_dict["resources.csv"] = df_res.to_csv(index=False)
        
    # 3. Assignments CSV
    assignments_rows = []
    for algo_name, algo_data in payload.get("algorithms", {}).items():
        for asgn in algo_data.get("assignments", []):
            assignments_rows.append({
                "algorithm": algo_name,
                "incident_id": asgn.get("incident_id"),
                "incident_name": asgn.get("incident_name"),
                "assigned_resource_ids": "; ".join(asgn.get("resource_ids", [])),
                "assigned_resource_names": "; ".join(asgn.get("resource_names", [])),
                "travel_time_min": asgn.get("estimated_travel_time_min"),
                "total_response_time_min": asgn.get("total_response_time_min"),
                "operating_cost": asgn.get("operating_cost"),
                "is_fully_served": asgn.get("is_fully_served"),
                "missing_resources": "; ".join(asgn.get("missing_resource_types", [])),
            })
    if assignments_rows:
        df_asgn = pd.DataFrame(assignments_rows)
        csv_dict["assignments.csv"] = df_asgn.to_csv(index=False)
        
    # 4. Summary CSV
    summary_rows = []
    for algo_name, algo_data in payload.get("algorithms", {}).items():
        summary_rows.append({
            "algorithm": algo_name,
            "status": algo_data.get("status"),
            "is_feasible": algo_data.get("is_feasible"),
            "served_count": len(algo_data.get("served_incident_ids", [])),
            "unserved_count": len(algo_data.get("unserved_incident_ids", [])),
            "weighted_response_time_min": algo_data.get("total_weighted_response_time"),
            "operating_cost": algo_data.get("total_operating_cost"),
            "objective_value": algo_data.get("objective_value"),
            "resource_utilization_rate": algo_data.get("resource_utilization_rate"),
            "runtime_sec": algo_data.get("runtime_sec"),
            "violations_count": len(algo_data.get("constraint_violations", [])),
        })
    if summary_rows:
        df_summary = pd.DataFrame(summary_rows)
        csv_dict["algorithm_comparison.csv"] = df_summary.to_csv(index=False)
        
    return csv_dict


def generate_markdown_report(payload: Dict[str, Any]) -> str:
    """Generates an executive markdown report suitable for judges, audit, and presentation."""
    scen = payload["scenario"]
    algorithms = payload.get("algorithms", {})
    
    lines = [
        f"# QRescue: Disaster Response Optimization Report",
        f"**Experiment ID:** `{payload['experiment_id']}`  ",
        f"**Generated:** {payload['timestamp']}  ",
        f"**Scenario:** {scen['name']} ({scen['scenario_type']})  ",
        f"**Congestion Multiplier:** {scen['road_congestion_factor']}x | **Weather:** {scen['weather_impact']}  ",
        "",
        "---",
        "## 1. Executive Summary",
        f"This experiment simulated an emergency event comprising **{len(payload['incidents'])} incidents** "
        f"and **{len(payload['resources'])} deployable response resources**. "
        "Three optimization strategies were executed on identical parameters to analyze dispatch efficiency, "
        "constraint satisfaction, and quantum approximate optimization feasibility.",
        "",
        "## 2. Algorithm Performance Comparison",
        "",
        "| Algorithm | Status | Feasible? | Served | Unserved | Weighted Time (min) | Cost ($) | Objective | Runtime (s) |",
        "| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |",
    ]
    
    for name, data in algorithms.items():
        lines.append(
            f"| **{name}** | {data.get('status')} | {'Yes' if data.get('is_feasible') else 'No'} | "
            f"{len(data.get('served_incident_ids', []))} | {len(data.get('unserved_incident_ids', []))} | "
            f"{data.get('total_weighted_response_time', 0.0):.1f} | ${data.get('total_operating_cost', 0.0):.2f} | "
            f"{data.get('objective_value', 0.0):.2f} | {data.get('runtime_sec', 0.0):.4f}s |"
        )
        
    lines.extend([
        "",
        "## 3. Incident Triage Breakdown",
        "",
        "| ID | Incident Name | Category | Sev | People | Priority Score | Req. Resources |",
        "| :--- | :--- | :--- | :---: | :---: | :---: | :--- |",
    ])
    
    for inc in payload.get("incidents", []):
        req_str = ", ".join(inc.get("required_resource_types", []))
        lines.append(
            f"| `{inc.get('id')}` | {inc.get('name')} | {inc.get('category')} | "
            f"{inc.get('severity')}/5 | {inc.get('people_affected')} | "
            f"{inc.get('urgency_score', 0.0):.1f} ({inc.get('priority_category')}) | {req_str} |"
        )
        
    lines.extend([
        "",
        "## 4. Scientific Assumptions & Disclaimers",
        "",
        "> [!IMPORTANT]",
        "> **Educational & Research Prototype:** QRescue is designed strictly for comparative research in "
        "> mathematical and quantum optimization. It is NOT validated for real-world emergency dispatch.",
        "",
        "- **Travel Estimation:** Straight-line Haversine distance is adjusted with a 1.35x curvature multiplier, "
        "nominal fleet speeds, terrain access difficulty, and dynamic flood/rubble congestion factors.",
        "- **Quantum Simulation:** QAOA execution was run using Qiskit Aer on classical CPU simulation. "
        "Measured execution times include classical matrix simulation overhead and cannot establish physical quantum hardware speedup.",
        "- **Objective Function:** Penalizes unserved critical emergencies, minimizes transit delay, and accounts for operational resource expenditures.",
        "",
        "---",
        "*Report automatically generated by QRescue Simulation Platform.*",
    ])
    
    return "\n".join(lines)
