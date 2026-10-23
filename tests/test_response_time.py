"""
Unit tests for Response-Time Estimation model.
"""

import pytest
from src.data_models import Incident, Resource, DisasterCategory, ResourceType
from src.response_time import (
    haversine_distance_km,
    estimate_travel_distance,
    estimate_transit_time_minutes,
    calculate_incident_resource_response,
    compute_cost_matrix,
    ROAD_NETWORK_DETOUR_FACTOR,
)


def test_haversine_and_detour_distance():
    # San Francisco to Oakland approx 13-14 km straight line
    lat1, lon1 = 37.7749, -122.4194
    lat2, lon2 = 37.8044, -122.2712
    
    dist_straight = haversine_distance_km(lat1, lon1, lat2, lon2)
    assert 10.0 <= dist_straight <= 20.0
    
    dist_road = estimate_travel_distance((lat1, lon1), (lat2, lon2), apply_road_detour=True)
    assert dist_road == pytest.approx(dist_straight * ROAD_NETWORK_DETOUR_FACTOR, rel=1e-3)
    assert dist_road > dist_straight


def test_transit_time_calculation():
    # 30 km distance at 60 km/h with 1.0 congestion and 1.0 access = 30 minutes
    time_normal = estimate_transit_time_minutes(
        distance_km=30.0,
        resource_speed_kmh=60.0,
        congestion_factor=1.0,
        access_difficulty=1.0,
    )
    assert time_normal == pytest.approx(30.0, abs=0.1)

    # 30 km distance with 1.5 congestion = 45 minutes
    time_congested = estimate_transit_time_minutes(
        distance_km=30.0,
        resource_speed_kmh=60.0,
        congestion_factor=1.5,
        access_difficulty=1.0,
    )
    assert time_congested == pytest.approx(45.0, abs=0.1)


def test_incident_resource_response_calculation():
    inc = Incident(
        id="INC-1",
        name="Flood site",
        category=DisasterCategory.FLOOD.value,
        lat=37.77,
        lon=-122.41,
        people_affected=10,
        severity=3,
        estimated_service_duration=25.0,
        access_difficulty=1.2,
    )
    res = Resource(
        id="RES-1",
        name="Ambulance Alpha",
        resource_type=ResourceType.AMBULANCE.value,
        lat=37.75,
        lon=-122.40,
        response_speed_kmh=60.0,
        operating_cost_per_hour=120.0,
    )
    metrics = calculate_incident_resource_response(inc, res, congestion_factor=1.3)
    
    assert metrics["distance_km"] > 0.0
    assert metrics["transit_time_min"] > 0.0
    assert metrics["total_response_time_min"] == pytest.approx(
        metrics["transit_time_min"] + inc.estimated_service_duration, abs=0.1
    )
    assert metrics["estimated_operating_cost"] > 0.0


def test_cost_matrix_dimensions():
    incidents = [
        Incident("I1", "N1", DisasterCategory.FIRE.value, 37.7, -122.4, 5, 3),
        Incident("I2", "N2", DisasterCategory.FIRE.value, 37.8, -122.5, 10, 4),
    ]
    resources = [
        Resource("R1", "Amb 1", ResourceType.AMBULANCE.value, 37.7, -122.4),
        Resource("R2", "Amb 2", ResourceType.AMBULANCE.value, 37.75, -122.45),
        Resource("R3", "Amb 3", ResourceType.AMBULANCE.value, 37.8, -122.3),
    ]
    matrix = compute_cost_matrix(incidents, resources)
    assert matrix.shape == (2, 3)
    assert matrix[0, 0] >= 0.0
