"""
Unit tests for constraint validation and classical optimization (Greedy and OR-Tools CP-SAT).
"""

import pytest
from src.data_models import (
    Incident,
    Resource,
    Assignment,
    DisasterCategory,
    ResourceType,
)
from src.classical_optimizer import (
    validate_assignments,
    run_greedy_baseline,
    run_ortools_optimizer,
)


def test_unavailable_resource_rejection():
    inc = Incident(
        id="INC-1",
        name="Fire",
        category=DisasterCategory.FIRE.value,
        lat=37.77,
        lon=-122.41,
        people_affected=10,
        severity=4,
        required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value],
    )
    # Unavailable resource
    res = Resource(
        id="RES-UNAVAIL",
        name="Broken Engine",
        resource_type=ResourceType.FIRE_RESPONSE_TEAM.value,
        lat=37.77,
        lon=-122.41,
        available=False,
    )
    asgn = Assignment(
        incident_id=inc.id,
        incident_name=inc.name,
        resource_ids=[res.id],
        resource_names=[res.name],
        estimated_travel_time_min=5.0,
        is_fully_served=True,
    )
    is_valid, violations = validate_assignments([inc], [res], [asgn])
    assert is_valid is False
    assert any("unavailable" in v.lower() for v in violations)


def test_exclusive_resource_conflict_detection():
    inc1 = Incident("INC-1", "Fire 1", DisasterCategory.FIRE.value, 37.7, -122.4, 5, 3,
                    required_resource_types=[ResourceType.AMBULANCE.value])
    inc2 = Incident("INC-2", "Fire 2", DisasterCategory.FIRE.value, 37.8, -122.4, 5, 3,
                    required_resource_types=[ResourceType.AMBULANCE.value])
    res = Resource("RES-AMB", "Solo Ambulance", ResourceType.AMBULANCE.value, 37.75, -122.4, available=True)

    # Assigning the SAME resource to two incidents
    asgns = [
        Assignment("INC-1", "Fire 1", ["RES-AMB"], ["Solo Ambulance"], 5.0, is_fully_served=True),
        Assignment("INC-2", "Fire 2", ["RES-AMB"], ["Solo Ambulance"], 10.0, is_fully_served=True),
    ]
    is_valid, violations = validate_assignments([inc1, inc2], [res], asgns)
    assert is_valid is False
    assert any("conflict" in v.lower() or "multiple" in v.lower() for v in violations)


def test_capability_mismatch_detection():
    inc = Incident("INC-1", "Collapse", DisasterCategory.BUILDING_COLLAPSE.value, 37.7, -122.4, 10, 4,
                   required_resource_types=[ResourceType.RESCUE_TEAM.value])
    # Supply unit cannot do rescue
    res = Resource("RES-SUPPLY", "Medical Supply", ResourceType.MEDICAL_SUPPLY_UNIT.value, 37.7, -122.4, available=True)

    asgn = Assignment("INC-1", "Collapse", ["RES-SUPPLY"], ["Medical Supply"], 5.0, is_fully_served=True)
    is_valid, violations = validate_assignments([inc], [res], [asgn])
    assert is_valid is False
    assert any("mismatch" in v.lower() for v in violations)


def test_multi_resource_requirement_fulfillment():
    inc = Incident("INC-MULTI", "Major Disaster", DisasterCategory.FLOOD.value, 37.7, -122.4, 30, 5,
                   required_resource_types=[ResourceType.RESCUE_TEAM.value, ResourceType.AMBULANCE.value])
    res_rsc = Resource("RES-R1", "Rescue 1", ResourceType.RESCUE_TEAM.value, 37.7, -122.4, available=True)
    res_amb = Resource("RES-A1", "Ambulance 1", ResourceType.AMBULANCE.value, 37.7, -122.4, available=True)

    # Partial assignment: only rescue team, but claiming fully served
    asgn_partial = Assignment(
        incident_id=inc.id,
        incident_name=inc.name,
        resource_ids=[res_rsc.id],
        resource_names=[res_rsc.name],
        estimated_travel_time_min=5.0,
        is_fully_served=True,  # Inconsistent!
    )
    is_valid, violations = validate_assignments([inc], [res_rsc, res_amb], [asgn_partial])
    assert is_valid is False
    assert any("inconsistency" in v.lower() for v in violations)


def test_empty_incidents_or_resources():
    res_empty_inc = run_ortools_optimizer([], [Resource("R1", "Amb", ResourceType.AMBULANCE.value, 37.7, -122.4)])
    assert res_empty_inc.status == "NO_SOLUTION"
    assert res_empty_inc.is_feasible is False

    res_empty_res = run_ortools_optimizer([Incident("I1", "Name", DisasterCategory.FIRE.value, 37.7, -122.4, 5, 3)], [])
    assert res_empty_res.status == "NO_SOLUTION"
    assert res_empty_res.is_feasible is False


def test_classical_optimizer_on_multi_hazard():
    from src.sample_data import get_scenario_multihazard
    scen = get_scenario_multihazard()
    
    result = run_ortools_optimizer(scen.incidents, scen.resources)
    assert result.status in ["OPTIMAL", "FEASIBLE"]
    assert result.is_feasible is True
    assert len(result.served_incident_ids) > 0
    assert result.objective_value > 0.0
    assert result.runtime_sec >= 0.0
