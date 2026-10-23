"""
Data models for the QRescue disaster response simulation platform.
Defines Incidents, Resources, Assignments, Scenarios, and Optimization results.
"""

from __future__ import annotations
from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Dict, Any, Optional
import math


class DisasterCategory(str, Enum):
    FLOOD = "Flood"
    LANDSLIDE = "Landslide"
    FIRE = "Fire"
    ROAD_ACCIDENT = "Road accident"
    BUILDING_COLLAPSE = "Building collapse"
    MEDICAL_EMERGENCY = "Medical emergency"


class ResourceType(str, Enum):
    AMBULANCE = "Ambulance"
    RESCUE_TEAM = "Rescue team"
    FIRE_RESPONSE_TEAM = "Fire-response team"
    MEDICAL_SUPPLY_UNIT = "Medical supply unit"


class PriorityLevel(str, Enum):
    CRITICAL = "Critical"
    HIGH = "High"
    MEDIUM = "Medium"
    LOW = "Low"


# Default resource capability mapping
RESOURCE_CAPABILITIES: Dict[ResourceType, List[str]] = {
    ResourceType.AMBULANCE: ["medical_transport", "triage", "advanced_life_support"],
    ResourceType.RESCUE_TEAM: ["heavy_extrication", "flood_rescue", "structural_search", "technical_rope_rescue"],
    ResourceType.FIRE_RESPONSE_TEAM: ["fire_suppression", "hazmat_containment", "smoke_clearing"],
    ResourceType.MEDICAL_SUPPLY_UNIT: ["bulk_triage_supplies", "oxygen_distribution", "blood_field_kits"],
}


@dataclass
class Incident:
    id: str
    name: str
    category: str
    lat: float
    lon: float
    people_affected: int
    severity: int  # 1 to 5 scale
    urgency_score: float = 0.0  # 0 to 100 simulation score
    required_resource_types: List[str] = field(default_factory=list)
    estimated_service_duration: float = 30.0  # minutes
    status: str = "Pending"  # "Pending", "Assigned", "In Progress", "Resolved", "Unserved"
    time_sensitivity: int = 3  # 1 to 5 scale
    access_difficulty: float = 1.0  # 1.0 (normal) to 3.0 (severe terrain / blocked roads)
    priority_category: str = "Medium"
    priority_factors: Dict[str, float] = field(default_factory=dict)
    priority_explanation: str = ""

    def validate(self) -> List[str]:
        """Validate incident attributes and return error messages if any."""
        errors: List[str] = []
        if not self.id or not isinstance(self.id, str):
            errors.append("Incident ID must be a non-empty string.")
        if not self.name or not isinstance(self.name, str):
            errors.append("Incident name must be a non-empty string.")
        
        valid_categories = [c.value for c in DisasterCategory]
        if self.category not in valid_categories:
            errors.append(f"Category '{self.category}' must be one of {valid_categories}.")
            
        if not (-90.0 <= self.lat <= 90.0):
            errors.append(f"Latitude {self.lat} must be between -90 and 90.")
        if not (-180.0 <= self.lon <= 180.0):
            errors.append(f"Longitude {self.lon} must be between -180 and 180.")
            
        if self.people_affected < 0:
            errors.append(f"People affected ({self.people_affected}) cannot be negative.")
            
        if not (1 <= self.severity <= 5):
            errors.append(f"Severity ({self.severity}) must be an integer between 1 and 5.")
            
        if not (1 <= self.time_sensitivity <= 5):
            errors.append(f"Time sensitivity ({self.time_sensitivity}) must be between 1 and 5.")
            
        if self.estimated_service_duration <= 0:
            errors.append(f"Estimated service duration ({self.estimated_service_duration}) must be > 0.")
            
        if self.access_difficulty < 1.0 or self.access_difficulty > 5.0:
            errors.append(f"Access difficulty ({self.access_difficulty}) must be between 1.0 and 5.0.")

        valid_types = [t.value for t in ResourceType]
        for rt in self.required_resource_types:
            if rt not in valid_types:
                errors.append(f"Required resource type '{rt}' must be one of {valid_types}.")
                
        return errors

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Incident:
        # Filter fields matching dataclass attributes
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)


@dataclass
class Resource:
    id: str
    name: str
    resource_type: str
    lat: float
    lon: float
    available: bool = True
    capacity: int = 4  # e.g., max people transportable or treated
    operational_capabilities: List[str] = field(default_factory=list)
    operating_cost_per_hour: float = 120.0  # simulated cost in $/hr
    response_speed_kmh: float = 50.0  # nominal speed km/h
    assignment_status: str = "Available"  # "Available", "Assigned", "Unavailable"
    assigned_incident_id: Optional[str] = None

    def validate(self) -> List[str]:
        """Validate resource attributes and return error messages if any."""
        errors: List[str] = []
        if not self.id or not isinstance(self.id, str):
            errors.append("Resource ID must be a non-empty string.")
        if not self.name or not isinstance(self.name, str):
            errors.append("Resource name must be a non-empty string.")
            
        valid_types = [t.value for t in ResourceType]
        if self.resource_type not in valid_types:
            errors.append(f"Resource type '{self.resource_type}' must be one of {valid_types}.")
            
        if not (-90.0 <= self.lat <= 90.0):
            errors.append(f"Latitude {self.lat} must be between -90 and 90.")
        if not (-180.0 <= self.lon <= 180.0):
            errors.append(f"Longitude {self.lon} must be between -180 and 180.")
            
        if self.capacity <= 0:
            errors.append(f"Capacity ({self.capacity}) must be greater than 0.")
            
        if self.operating_cost_per_hour < 0:
            errors.append(f"Operating cost per hour ({self.operating_cost_per_hour}) cannot be negative.")
            
        if self.response_speed_kmh <= 0:
            errors.append(f"Response speed ({self.response_speed_kmh}) must be > 0.")
            
        return errors

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Resource:
        valid_keys = {f.name for f in cls.__dataclass_fields__.values()}
        filtered = {k: v for k, v in data.items() if k in valid_keys}
        return cls(**filtered)


@dataclass
class Assignment:
    incident_id: str
    incident_name: str
    resource_ids: List[str]
    resource_names: List[str]
    estimated_travel_time_min: float
    total_response_time_min: float = 0.0
    total_service_time_min: float = 0.0
    operating_cost: float = 0.0
    is_fully_served: bool = False
    missing_resource_types: List[str] = field(default_factory=list)
    assignment_details: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class OptimizationResult:
    algorithm_name: str
    status: str  # "OPTIMAL", "FEASIBLE", "INFEASIBLE", "NO_SOLUTION"
    assignments: List[Assignment]
    served_incident_ids: List[str]
    unserved_incident_ids: List[str]
    total_weighted_response_time: float
    total_operating_cost: float
    objective_value: float
    resource_utilization_rate: float  # 0.0 to 1.0 (or %)
    runtime_sec: float
    constraint_violations: List[str] = field(default_factory=list)
    is_feasible: bool = True
    metadata: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Scenario:
    id: str
    name: str
    description: str
    scenario_type: str
    incidents: List[Incident]
    resources: List[Resource]
    road_congestion_factor: float = 1.2
    weather_impact: str = "Moderate rain"
    random_seed: int = 42

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "scenario_type": self.scenario_type,
            "road_congestion_factor": self.road_congestion_factor,
            "weather_impact": self.weather_impact,
            "random_seed": self.random_seed,
            "incidents": [inc.to_dict() for inc in self.incidents],
            "resources": [res.to_dict() for res in self.resources],
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Scenario:
        incidents = [Incident.from_dict(i) for i in data.get("incidents", [])]
        resources = [Resource.from_dict(r) for r in data.get("resources", [])]
        return cls(
            id=data["id"],
            name=data["name"],
            description=data.get("description", ""),
            scenario_type=data.get("scenario_type", "Custom"),
            incidents=incidents,
            resources=resources,
            road_congestion_factor=float(data.get("road_congestion_factor", 1.2)),
            weather_impact=data.get("weather_impact", "Normal"),
            random_seed=int(data.get("random_seed", 42)),
        )
