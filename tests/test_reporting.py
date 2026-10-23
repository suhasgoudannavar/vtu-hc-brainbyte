"""
Unit tests for Experiment Reporting, CSV, JSON, and Markdown generation.
"""

import json
import pytest
from src.sample_data import get_scenario_urban_flood
from src.classical_optimizer import run_greedy_baseline, run_ortools_optimizer
from src.reporting import (
    create_experiment_payload,
    export_experiment_json,
    export_experiment_csv_bundle,
    generate_markdown_report,
)


def test_experiment_payload_and_json_export():
    scen = get_scenario_urban_flood()
    res1 = run_greedy_baseline(scen.incidents, scen.resources)
    res2 = run_ortools_optimizer(scen.incidents, scen.resources)
    
    payload = create_experiment_payload(
        scenario=scen,
        results={"Greedy": res1, "OR-Tools": res2},
        selected_algorithm="OR-Tools",
    )
    
    assert "experiment_id" in payload
    assert len(payload["incidents"]) == len(scen.incidents)
    assert len(payload["resources"]) == len(scen.resources)
    assert "OR-Tools" in payload["algorithms"]

    # Test JSON string conversion
    json_str = export_experiment_json(payload)
    parsed = json.loads(json_str)
    assert parsed["experiment_id"] == payload["experiment_id"]


def test_csv_bundle_export():
    scen = get_scenario_urban_flood()
    res = run_ortools_optimizer(scen.incidents, scen.resources)
    payload = create_experiment_payload(scenario=scen, results={"OR-Tools": res})

    csv_bundle = export_experiment_csv_bundle(payload)
    assert "incidents.csv" in csv_bundle
    assert "resources.csv" in csv_bundle
    assert "assignments.csv" in csv_bundle
    assert "algorithm_comparison.csv" in csv_bundle
    
    assert "INC-FL-01" in csv_bundle["incidents.csv"]
    assert "RES-AMB-01" in csv_bundle["resources.csv"]


def test_markdown_report_generation():
    scen = get_scenario_urban_flood()
    res = run_ortools_optimizer(scen.incidents, scen.resources)
    payload = create_experiment_payload(scenario=scen, results={"OR-Tools": res})

    md_report = generate_markdown_report(payload)
    assert "# QRescue: Disaster Response Optimization Report" in md_report
    assert "Algorithm Performance Comparison" in md_report
    assert "Scientific Assumptions & Disclaimers" in md_report
