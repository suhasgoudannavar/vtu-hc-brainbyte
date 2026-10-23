"""
Tests for UI chart helpers, scenario presets, and compilation of app.py.
"""

import py_compile
import pytest
from src.sample_data import (
    get_scenario_urban_flood,
    get_scenario_landslide,
    get_scenario_multihazard,
    get_scenario_resource_shortage,
    generate_custom_scenario,
)
from src.classical_optimizer import run_ortools_optimizer
from src.evaluation import run_full_comparison
from src.ui_helpers import (
    render_spatial_simulation_map,
    render_incident_severity_chart,
    render_resource_utilization_chart,
    render_response_time_analysis_chart,
    render_incident_priority_matrix,
    render_comparison_charts,
    render_quantum_distribution_chart,
    render_experiment_history_chart,
)


def test_app_py_compilation():
    """Verify app.py has valid Python syntax and compiles without error."""
    py_compile.compile("app.py", doraise=True)


def test_resource_shortage_scenario_and_solver():
    """Verify the new Resource Shortage scenario runs and is solvable."""
    scen = get_scenario_resource_shortage()
    assert len(scen.incidents) == 6
    assert len(scen.resources) == 5
    assert sum(1 for r in scen.resources if r.available) == 3
    assert sum(1 for r in scen.resources if not r.available) == 2

    res = run_ortools_optimizer(scen.incidents, scen.resources, scen.road_congestion_factor)
    assert res.is_feasible is True
    assert len(res.constraint_violations) == 0
    # Because units are limited (3 available), some incidents must remain unserved
    assert len(res.served_incident_ids) > 0
    assert len(res.unserved_incident_ids) > 0


def test_all_ui_chart_renderers():
    """Verify all chart renderers produce valid Plotly figures without error."""
    scen = get_scenario_urban_flood()
    res = run_ortools_optimizer(scen.incidents, scen.resources, scen.road_congestion_factor)

    # 1. Spatial map
    fig_map = render_spatial_simulation_map(
        incidents=scen.incidents,
        resources=scen.resources,
        assignments=res.assignments,
    )
    assert fig_map is not None

    # 2. Incident severity chart
    fig_sev = render_incident_severity_chart(scen.incidents)
    assert fig_sev is not None

    # 3. Resource utilization chart
    fig_util = render_resource_utilization_chart(scen.resources, res.assignments)
    assert fig_util is not None

    # 4. Response time analysis chart
    fig_resp = render_response_time_analysis_chart(res.assignments, scen.incidents)
    assert fig_resp is not None

    # 5. Incident priority matrix
    fig_prior = render_incident_priority_matrix(scen.incidents)
    assert fig_prior is not None

    # 6. Comparison charts
    comp = run_full_comparison(
        incidents=scen.incidents,
        resources=scen.resources,
        congestion_factor=scen.road_congestion_factor,
        include_quantum=False,
    )
    fig1, fig2, fig3 = render_comparison_charts(comp)
    assert fig1 is not None
    assert fig2 is not None
    assert fig3 is not None

    # 7. Quantum distribution chart
    candidates = [
        {"bitstring": "100100", "probability": 0.42, "cost": -12.5, "is_feasible": True},
        {"bitstring": "010010", "probability": 0.28, "cost": -8.0, "is_feasible": True},
    ]
    fig_q = render_quantum_distribution_chart(candidates)
    assert fig_q is not None

    # 8. Experiment history chart
    history = [
        {"algorithm": "OR-Tools", "served": 4, "objective": 120.5},
        {"algorithm": "Greedy", "served": 3, "objective": 150.2},
    ]
    fig_hist = render_experiment_history_chart(history)
    assert fig_hist is not None
