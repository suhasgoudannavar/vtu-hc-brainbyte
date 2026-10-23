"""
Response-Time Estimation Model for QRescue.
Calculates simulated travel distance, transit time, and total service duration.
Clearly distinguishes straight-line distance from simulated road network travel time.
"""

from __future__ import annotations
import math
from typing import Dict, List, Tuple
import numpy as np

from src.data_models import Incident, Resource, ResourceType


DEFAULT_SPEEDS_KMH: Dict[str, float] = {
    ResourceType.AMBULANCE.value: 60.0,
    ResourceType.FIRE_RESPONSE_TEAM.value: 50.0,
    ResourceType.RESCUE_TEAM.value: 45.0,
    ResourceType.MEDICAL_SUPPLY_UNIT.value: 55.0,
}

# Empirical detour / road curvature factor applied to straight-line distance
ROAD_NETWORK_DETOUR_FACTOR: float = 1.35


def haversine_distance_km(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Computes great-circle distance between two coordinates in kilometers.
    """
    R = 6371.0  # Earth's mean radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat / 2.0) ** 2 +
        math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2.0) ** 2
    )
    c = 2.0 * math.atan2(math.sqrt(a), math.sqrt(max(0.0, 1.0 - a)))
    return R * c


def estimate_travel_distance(
    loc1: Tuple[float, float],
    loc2: Tuple[float, float],
    apply_road_detour: bool = True,
) -> float:
    """
    Calculates estimated road distance between two coordinates.
    Applies a standard detour multiplier (1.35x) to approximate real road curvature.
    """
    straight_line = haversine_distance_km(loc1[0], loc1[1], loc2[0], loc2[1])
    if apply_road_detour:
        return straight_line * ROAD_NETWORK_DETOUR_FACTOR
    return straight_line


def estimate_transit_time_minutes(
    distance_km: float,
    resource_speed_kmh: float,
    congestion_factor: float = 1.2,
    access_difficulty: float = 1.0,
) -> float:
    """
    Estimates travel time in minutes based on distance, nominal speed,
    simulated road congestion, and terrain access difficulty.
    
    Formula:
        effective_speed = resource_speed / (congestion_factor * access_difficulty)
        travel_time_min = (distance_km / effective_speed) * 60.0
    """
    if resource_speed_kmh <= 0:
        return 999.0  # Unreachable / immobile
        
    c_factor = max(1.0, congestion_factor)
    a_factor = max(1.0, access_difficulty)
    effective_speed = resource_speed_kmh / (c_factor * a_factor)
    
    # Avoid zero division
    if effective_speed < 1.0:
        effective_speed = 1.0
        
    transit_hours = distance_km / effective_speed
    return transit_hours * 60.0


def calculate_incident_resource_response(
    incident: Incident,
    resource: Resource,
    congestion_factor: float = 1.2,
) -> Dict[str, float]:
    """
    Calculates detailed metrics for assigning a specific resource to an incident.
    """
    dist_km = estimate_travel_distance(
        (resource.lat, resource.lon),
        (incident.lat, incident.lon),
    )
    
    speed = resource.response_speed_kmh or DEFAULT_SPEEDS_KMH.get(resource.resource_type, 50.0)
    transit_min = estimate_transit_time_minutes(
        distance_km=dist_km,
        resource_speed_kmh=speed,
        congestion_factor=congestion_factor,
        access_difficulty=incident.access_difficulty,
    )
    
    total_service_min = transit_min + incident.estimated_service_duration
    cost = (total_service_min / 60.0) * resource.operating_cost_per_hour
    
    return {
        "distance_km": round(dist_km, 2),
        "transit_time_min": round(transit_min, 2),
        "total_response_time_min": round(total_service_min, 2),
        "estimated_operating_cost": round(cost, 2),
    }


def compute_cost_matrix(
    incidents: List[Incident],
    resources: List[Resource],
    congestion_factor: float = 1.2,
) -> np.ndarray:
    """
    Computes an (N_incidents x M_resources) transit time matrix in minutes.
    """
    n = len(incidents)
    m = len(resources)
    matrix = np.zeros((n, m), dtype=float)
    
    for i, inc in enumerate(incidents):
        for j, res in enumerate(resources):
            metrics = calculate_incident_resource_response(inc, res, congestion_factor)
            matrix[i, j] = metrics["transit_time_min"]
            
    return matrix
