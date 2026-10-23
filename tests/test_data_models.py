"""
Unit tests for data models, validation, and scenario instantiation.
"""

import pytest
from src.data_models import (
    Incident,
    Resource,
    DisasterCategory,
    ResourceType,
    PriorityLevel,
    Scenario,
)
from src.sample_data import (
    get_scenario_urban_flood,
    get_scenario_landslide,
    get_scenario_multihazard,
    generate_custom_scenario,
)


def test_valid_incident_creation():
    inc = Incident(
        id="INC-01",
        name="Test Incident",
        category=DisasterCategory.FLOOD.value,
        lat=37.77,
        lon=-122.41,
        people_affected=10,
        severity=4,
        required_resource_types=[ResourceType.AMBULANCE.value],
    )
    errors = inc.validate()
    assert len(errors) == 0


def test_invalid_incident_validation():
    # Negative people, invalid severity, out of range lat
    inc = Incident(
        id="",
        name="",
        category="Alien Invasion",  # invalid
        lat=150.0,  # invalid
        lon=-200.0,  # invalid
        people_affected=-5,
        severity=9,  # invalid
        required_resource_types=["Flying Saucer"],
        estimated_service_duration=-10.0,
    )
    errors = inc.validate()
    assert len(errors) >= 6
    assert any("Latitude" in e for e in errors)
    assert any("Severity" in e for e in errors)
    assert any("Category" in e for e in errors)


def test_resource_validation():
    res_valid = Resource(
        id="RES-01",
        name="Ambulance 1",
        resource_type=ResourceType.AMBULANCE.value,
        lat=37.77,
        lon=-122.42,
        available=True,
        capacity=4,
    )
    assert len(res_valid.validate()) == 0

    res_invalid = Resource(
        id="",
        name="",
        resource_type="Tank",
        lat=37.77,
        lon=-122.42,
        capacity=-1,
        operating_cost_per_hour=-50.0,
        response_speed_kmh=0.0,
    )
    errors = res_invalid.validate()
    assert len(errors) >= 4


def test_sample_scenarios_structure():
    scen_a = get_scenario_urban_flood()
    assert len(scen_a.incidents) == 5
    assert len(scen_a.resources) == 5
    assert scen_a.road_congestion_factor == 1.5

    scen_b = get_scenario_landslide()
    assert len(scen_b.incidents) >= 4
    assert len(scen_b.resources) >= 3

    scen_c = get_scenario_multihazard()
    assert len(scen_c.incidents) >= 6
    assert len(scen_c.resources) >= 6


def test_custom_scenario_generator():
    scen = generate_custom_scenario(n_incidents=7, n_resources=4, random_seed=99)
    assert len(scen.incidents) == 7
    assert len(scen.resources) == 4
    for inc in scen.incidents:
        assert len(inc.validate()) == 0
    for res in scen.resources:
        assert len(res.validate()) == 0
