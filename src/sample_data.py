"""
Predefined and dynamically generated disaster response scenarios for QRescue.
Includes:
- Scenario A: Urban Flood
- Scenario B: Landslide
- Scenario C: Multi-Hazard Emergency
- Configurable synthetic scenario generator
All scenarios use synthetic coordinates clearly marked as simulated.
"""

from __future__ import annotations
import random
from typing import List, Dict, Any, Optional
import numpy as np

from src.data_models import (
    Incident,
    Resource,
    Scenario,
    DisasterCategory,
    ResourceType,
    RESOURCE_CAPABILITIES,
)
from src.prioritization import prioritize_incident


# Synthetic regional center (Metropolitan River Valley)
BASE_LAT: float = 37.7749
BASE_LON: float = -122.4194


def get_scenario_urban_flood() -> Scenario:
    """
    SCENARIO A: Urban Flood
    Downtown flash floods and riverside community inundation.
    Contention for rescue boats/teams and medical evacuations.
    """
    incidents = [
        Incident(
            id="INC-FL-01",
            name="Downtown Metro Station Inundation",
            category=DisasterCategory.FLOOD.value,
            lat=BASE_LAT + 0.015,
            lon=BASE_LON - 0.010,
            people_affected=85,
            severity=5,
            required_resource_types=[ResourceType.RESCUE_TEAM.value, ResourceType.AMBULANCE.value],
            estimated_service_duration=55.0,
            time_sensitivity=5,
            access_difficulty=1.8,
        ),
        Incident(
            id="INC-FL-02",
            name="Riverside Senior Living Evacuation",
            category=DisasterCategory.FLOOD.value,
            lat=BASE_LAT - 0.025,
            lon=BASE_LON + 0.030,
            people_affected=40,
            severity=4,
            required_resource_types=[ResourceType.AMBULANCE.value, ResourceType.MEDICAL_SUPPLY_UNIT.value],
            estimated_service_duration=45.0,
            time_sensitivity=4,
            access_difficulty=1.4,
        ),
        Incident(
            id="INC-FL-03",
            name="Submerged Highway Underpass Trapped Vehicles",
            category=DisasterCategory.FLOOD.value,
            lat=BASE_LAT + 0.035,
            lon=BASE_LON + 0.015,
            people_affected=14,
            severity=3,
            required_resource_types=[ResourceType.RESCUE_TEAM.value],
            estimated_service_duration=35.0,
            time_sensitivity=4,
            access_difficulty=1.6,
        ),
        Incident(
            id="INC-FL-04",
            name="Residential Basement Flooding & Power Loss",
            category=DisasterCategory.FLOOD.value,
            lat=BASE_LAT - 0.010,
            lon=BASE_LON - 0.025,
            people_affected=18,
            severity=2,
            required_resource_types=[ResourceType.RESCUE_TEAM.value],
            estimated_service_duration=25.0,
            time_sensitivity=2,
            access_difficulty=1.1,
        ),
        Incident(
            id="INC-FL-05",
            name="Isolated School Shelter Water Shortage",
            category=DisasterCategory.FLOOD.value,
            lat=BASE_LAT + 0.045,
            lon=BASE_LON - 0.035,
            people_affected=65,
            severity=3,
            required_resource_types=[ResourceType.MEDICAL_SUPPLY_UNIT.value],
            estimated_service_duration=30.0,
            time_sensitivity=3,
            access_difficulty=1.5,
        ),
    ]

    resources = [
        Resource(
            id="RES-AMB-01",
            name="Paramedic Ambulance Alpha",
            resource_type=ResourceType.AMBULANCE.value,
            lat=BASE_LAT,
            lon=BASE_LON,
            available=True,
            capacity=4,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.AMBULANCE],
            operating_cost_per_hour=140.0,
            response_speed_kmh=60.0,
        ),
        Resource(
            id="RES-AMB-02",
            name="Paramedic Ambulance Beta",
            resource_type=ResourceType.AMBULANCE.value,
            lat=BASE_LAT - 0.015,
            lon=BASE_LON + 0.010,
            available=True,
            capacity=4,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.AMBULANCE],
            operating_cost_per_hour=140.0,
            response_speed_kmh=58.0,
        ),
        Resource(
            id="RES-RSC-01",
            name="Swiftwater Rescue Squad 1",
            resource_type=ResourceType.RESCUE_TEAM.value,
            lat=BASE_LAT + 0.010,
            lon=BASE_LON + 0.020,
            available=True,
            capacity=8,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.RESCUE_TEAM],
            operating_cost_per_hour=190.0,
            response_speed_kmh=45.0,
        ),
        Resource(
            id="RES-RSC-02",
            name="Flood Extrication Unit 2",
            resource_type=ResourceType.RESCUE_TEAM.value,
            lat=BASE_LAT - 0.030,
            lon=BASE_LON - 0.015,
            available=False,  # Intentionally unavailable resource to test constraint!
            capacity=6,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.RESCUE_TEAM],
            operating_cost_per_hour=185.0,
            response_speed_kmh=45.0,
            assignment_status="Unavailable",
        ),
        Resource(
            id="RES-MED-01",
            name="Mobile Emergency Medical Depot",
            resource_type=ResourceType.MEDICAL_SUPPLY_UNIT.value,
            lat=BASE_LAT + 0.020,
            lon=BASE_LON - 0.020,
            available=True,
            capacity=15,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.MEDICAL_SUPPLY_UNIT],
            operating_cost_per_hour=110.0,
            response_speed_kmh=50.0,
        ),
    ]

    for inc in incidents:
        prioritize_incident(inc)

    return Scenario(
        id="SCENARIO-A",
        name="Scenario A: Urban Flood Crisis",
        description="Flash flooding across metropolitan lowlands with high-risk senior housing and transit bottlenecks.",
        scenario_type="Urban Flood",
        incidents=incidents,
        resources=resources,
        road_congestion_factor=1.5,
        weather_impact="Heavy downpour & standing water",
        random_seed=101,
    )


def get_scenario_landslide() -> Scenario:
    """
    SCENARIO B: Mountain Highway Landslide
    High access difficulty, severed mountain roads, urgent technical rescue needed.
    """
    incidents = [
        Incident(
            id="INC-LS-01",
            name="Hillside Pass Highway Mudslide Burial",
            category=DisasterCategory.LANDSLIDE.value,
            lat=BASE_LAT + 0.050,
            lon=BASE_LON + 0.040,
            people_affected=22,
            severity=5,
            required_resource_types=[ResourceType.RESCUE_TEAM.value, ResourceType.AMBULANCE.value],
            estimated_service_duration=75.0,
            time_sensitivity=5,
            access_difficulty=2.6,
        ),
        Incident(
            id="INC-LS-02",
            name="Mountain Foothill Cabin Settlement Cut Off",
            category=DisasterCategory.LANDSLIDE.value,
            lat=BASE_LAT + 0.065,
            lon=BASE_LON + 0.025,
            people_affected=35,
            severity=4,
            required_resource_types=[ResourceType.MEDICAL_SUPPLY_UNIT.value, ResourceType.RESCUE_TEAM.value],
            estimated_service_duration=50.0,
            time_sensitivity=4,
            access_difficulty=2.3,
        ),
        Incident(
            id="INC-LS-03",
            name="Bridge Approach Structural Soil Slump",
            category=DisasterCategory.LANDSLIDE.value,
            lat=BASE_LAT + 0.035,
            lon=BASE_LON + 0.055,
            people_affected=8,
            severity=3,
            required_resource_types=[ResourceType.RESCUE_TEAM.value],
            estimated_service_duration=40.0,
            time_sensitivity=3,
            access_difficulty=1.9,
        ),
        Incident(
            id="INC-LS-04",
            name="Secondary Road Debris Medical Emergency",
            category=DisasterCategory.MEDICAL_EMERGENCY.value,
            lat=BASE_LAT + 0.020,
            lon=BASE_LON + 0.030,
            people_affected=3,
            severity=4,
            required_resource_types=[ResourceType.AMBULANCE.value],
            estimated_service_duration=30.0,
            time_sensitivity=5,
            access_difficulty=1.7,
        ),
    ]

    resources = [
        Resource(
            id="RES-AMB-01",
            name="4x4 All-Terrain Ambulance Unit",
            resource_type=ResourceType.AMBULANCE.value,
            lat=BASE_LAT + 0.010,
            lon=BASE_LON + 0.015,
            available=True,
            capacity=3,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.AMBULANCE],
            operating_cost_per_hour=160.0,
            response_speed_kmh=52.0,
        ),
        Resource(
            id="RES-RSC-01",
            name="Alpine Heavy Search & Rescue Team",
            resource_type=ResourceType.RESCUE_TEAM.value,
            lat=BASE_LAT + 0.020,
            lon=BASE_LON + 0.010,
            available=True,
            capacity=10,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.RESCUE_TEAM],
            operating_cost_per_hour=210.0,
            response_speed_kmh=42.0,
        ),
        Resource(
            id="RES-MED-01",
            name="Field Trauma Supply Unit",
            resource_type=ResourceType.MEDICAL_SUPPLY_UNIT.value,
            lat=BASE_LAT,
            lon=BASE_LON,
            available=True,
            capacity=12,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.MEDICAL_SUPPLY_UNIT],
            operating_cost_per_hour=115.0,
            response_speed_kmh=48.0,
        ),
    ]

    for inc in incidents:
        prioritize_incident(inc)

    return Scenario(
        id="SCENARIO-B",
        name="Scenario B: Steep Ridge Landslide",
        description="Mass movement of soil and boulders blocking mountain arteries and threatening isolated hamlets.",
        scenario_type="Landslide",
        incidents=incidents,
        resources=resources,
        road_congestion_factor=1.8,
        weather_impact="Continuous slope instability",
        random_seed=202,
    )


def get_scenario_multihazard() -> Scenario:
    """
    SCENARIO C: Multi-Hazard Emergency
    Cascading emergency: industrial fire, building collapse, roadway pileup.
    Severe resource contention requiring balanced prioritization.
    """
    incidents = [
        Incident(
            id="INC-MH-01",
            name="Industrial Chemical Warehouse Fire",
            category=DisasterCategory.FIRE.value,
            lat=BASE_LAT - 0.015,
            lon=BASE_LON - 0.020,
            people_affected=45,
            severity=5,
            required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value, ResourceType.AMBULANCE.value],
            estimated_service_duration=60.0,
            time_sensitivity=5,
            access_difficulty=1.3,
        ),
        Incident(
            id="INC-MH-02",
            name="Old Commercial Mall Ceiling Collapse",
            category=DisasterCategory.BUILDING_COLLAPSE.value,
            lat=BASE_LAT + 0.010,
            lon=BASE_LON + 0.012,
            people_affected=70,
            severity=5,
            required_resource_types=[ResourceType.RESCUE_TEAM.value, ResourceType.AMBULANCE.value],
            estimated_service_duration=80.0,
            time_sensitivity=5,
            access_difficulty=1.5,
        ),
        Incident(
            id="INC-MH-03",
            name="Interstate Multi-Vehicle Collision",
            category=DisasterCategory.ROAD_ACCIDENT.value,
            lat=BASE_LAT - 0.035,
            lon=BASE_LON + 0.025,
            people_affected=15,
            severity=4,
            required_resource_types=[ResourceType.AMBULANCE.value, ResourceType.RESCUE_TEAM.value],
            estimated_service_duration=40.0,
            time_sensitivity=4,
            access_difficulty=1.4,
        ),
        Incident(
            id="INC-MH-04",
            name="Suburban Residential Complex Smoke Inhalation",
            category=DisasterCategory.FIRE.value,
            lat=BASE_LAT - 0.025,
            lon=BASE_LON - 0.040,
            people_affected=28,
            severity=3,
            required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value, ResourceType.MEDICAL_SUPPLY_UNIT.value],
            estimated_service_duration=35.0,
            time_sensitivity=3,
            access_difficulty=1.2,
        ),
        Incident(
            id="INC-MH-05",
            name="Community Clinic Critical Generator Failure",
            category=DisasterCategory.MEDICAL_EMERGENCY.value,
            lat=BASE_LAT + 0.025,
            lon=BASE_LON - 0.015,
            people_affected=12,
            severity=4,
            required_resource_types=[ResourceType.MEDICAL_SUPPLY_UNIT.value],
            estimated_service_duration=30.0,
            time_sensitivity=4,
            access_difficulty=1.1,
        ),
        Incident(
            id="INC-MH-06",
            name="Minor Electrical Substation Flare",
            category=DisasterCategory.FIRE.value,
            lat=BASE_LAT + 0.038,
            lon=BASE_LON + 0.030,
            people_affected=4,
            severity=2,
            required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value],
            estimated_service_duration=20.0,
            time_sensitivity=2,
            access_difficulty=1.0,
        ),
    ]

    resources = [
        Resource(
            id="RES-AMB-01",
            name="Paramedic Unit Alpha",
            resource_type=ResourceType.AMBULANCE.value,
            lat=BASE_LAT,
            lon=BASE_LON,
            available=True,
            capacity=4,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.AMBULANCE],
            operating_cost_per_hour=140.0,
            response_speed_kmh=60.0,
        ),
        Resource(
            id="RES-AMB-02",
            name="Paramedic Unit Beta",
            resource_type=ResourceType.AMBULANCE.value,
            lat=BASE_LAT + 0.010,
            lon=BASE_LON - 0.010,
            available=True,
            capacity=4,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.AMBULANCE],
            operating_cost_per_hour=140.0,
            response_speed_kmh=58.0,
        ),
        Resource(
            id="RES-FIR-01",
            name="Pumper Truck Engine 7",
            resource_type=ResourceType.FIRE_RESPONSE_TEAM.value,
            lat=BASE_LAT - 0.010,
            lon=BASE_LON - 0.010,
            available=True,
            capacity=6,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.FIRE_RESPONSE_TEAM],
            operating_cost_per_hour=220.0,
            response_speed_kmh=50.0,
        ),
        Resource(
            id="RES-FIR-02",
            name="Ladder Company 12",
            resource_type=ResourceType.FIRE_RESPONSE_TEAM.value,
            lat=BASE_LAT + 0.020,
            lon=BASE_LON + 0.020,
            available=True,
            capacity=6,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.FIRE_RESPONSE_TEAM],
            operating_cost_per_hour=230.0,
            response_speed_kmh=48.0,
        ),
        Resource(
            id="RES-RSC-01",
            name="Structural Extrication Task Force",
            resource_type=ResourceType.RESCUE_TEAM.value,
            lat=BASE_LAT - 0.005,
            lon=BASE_LON + 0.015,
            available=True,
            capacity=8,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.RESCUE_TEAM],
            operating_cost_per_hour=195.0,
            response_speed_kmh=46.0,
        ),
        Resource(
            id="RES-MED-01",
            name="Rapid Supply Logistics Unit",
            resource_type=ResourceType.MEDICAL_SUPPLY_UNIT.value,
            lat=BASE_LAT - 0.020,
            lon=BASE_LON,
            available=True,
            capacity=15,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.MEDICAL_SUPPLY_UNIT],
            operating_cost_per_hour=110.0,
            response_speed_kmh=52.0,
        ),
    ]

    for inc in incidents:
        prioritize_incident(inc)

    return Scenario(
        id="SCENARIO-C",
        name="Scenario C: Multi-Hazard Urban Disaster",
        description="Complex cascading catastrophe with concurrent fire, structural collapse, and mass transit collisions.",
        scenario_type="Multi-Hazard Emergency",
        incidents=incidents,
        resources=resources,
        road_congestion_factor=1.6,
        weather_impact="High winds & dry heat",
        random_seed=303,
    )


def get_scenario_resource_shortage() -> Scenario:
    """
    SCENARIO D: Severe Resource Shortage & Triage Contention
    High casualty volume where urgent emergency calls outnumber active deployable units,
    demonstrating strict constraint satisfaction and prioritization tradeoffs.
    """
    incidents = [
        Incident(
            id="INC-RS-01",
            name="Major Regional Hospital Oxygen Pipeline Rupture",
            category=DisasterCategory.MEDICAL_EMERGENCY.value,
            lat=BASE_LAT + 0.012,
            lon=BASE_LON - 0.018,
            people_affected=95,
            severity=5,
            required_resource_types=[ResourceType.AMBULANCE.value, ResourceType.MEDICAL_SUPPLY_UNIT.value],
            estimated_service_duration=65.0,
            time_sensitivity=5,
            access_difficulty=1.2,
        ),
        Incident(
            id="INC-RS-02",
            name="Highway Flyover Structural Slab Collapse",
            category=DisasterCategory.BUILDING_COLLAPSE.value,
            lat=BASE_LAT - 0.022,
            lon=BASE_LON + 0.015,
            people_affected=52,
            severity=5,
            required_resource_types=[ResourceType.RESCUE_TEAM.value, ResourceType.AMBULANCE.value],
            estimated_service_duration=75.0,
            time_sensitivity=5,
            access_difficulty=1.8,
        ),
        Incident(
            id="INC-RS-03",
            name="Flash Flood Submerged Primary School",
            category=DisasterCategory.FLOOD.value,
            lat=BASE_LAT + 0.038,
            lon=BASE_LON + 0.022,
            people_affected=42,
            severity=4,
            required_resource_types=[ResourceType.RESCUE_TEAM.value],
            estimated_service_duration=50.0,
            time_sensitivity=4,
            access_difficulty=1.6,
        ),
        Incident(
            id="INC-RS-04",
            name="Multi-Story Residential Complex Fire",
            category=DisasterCategory.FIRE.value,
            lat=BASE_LAT - 0.032,
            lon=BASE_LON - 0.025,
            people_affected=28,
            severity=4,
            required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value, ResourceType.AMBULANCE.value],
            estimated_service_duration=45.0,
            time_sensitivity=4,
            access_difficulty=1.3,
        ),
        Incident(
            id="INC-RS-05",
            name="Industrial Ammonia Refrigeration Tank Venting",
            category=DisasterCategory.FIRE.value,
            lat=BASE_LAT + 0.025,
            lon=BASE_LON - 0.035,
            people_affected=15,
            severity=3,
            required_resource_types=[ResourceType.FIRE_RESPONSE_TEAM.value],
            estimated_service_duration=35.0,
            time_sensitivity=3,
            access_difficulty=1.1,
        ),
        Incident(
            id="INC-RS-06",
            name="Elderly Care Center Auxiliary Power Loss",
            category=DisasterCategory.MEDICAL_EMERGENCY.value,
            lat=BASE_LAT - 0.015,
            lon=BASE_LON + 0.035,
            people_affected=30,
            severity=3,
            required_resource_types=[ResourceType.MEDICAL_SUPPLY_UNIT.value],
            estimated_service_duration=30.0,
            time_sensitivity=3,
            access_difficulty=1.1,
        ),
    ]

    resources = [
        Resource(
            id="RES-AMB-01",
            name="Paramedic Ambulance Alpha",
            resource_type=ResourceType.AMBULANCE.value,
            lat=BASE_LAT,
            lon=BASE_LON,
            available=True,
            capacity=4,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.AMBULANCE],
            operating_cost_per_hour=140.0,
            response_speed_kmh=60.0,
        ),
        Resource(
            id="RES-RSC-01",
            name="Urban Search & Rescue Squad",
            resource_type=ResourceType.RESCUE_TEAM.value,
            lat=BASE_LAT + 0.010,
            lon=BASE_LON + 0.015,
            available=True,
            capacity=8,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.RESCUE_TEAM],
            operating_cost_per_hour=200.0,
            response_speed_kmh=45.0,
        ),
        Resource(
            id="RES-FIR-01",
            name="Engine Company 9",
            resource_type=ResourceType.FIRE_RESPONSE_TEAM.value,
            lat=BASE_LAT - 0.010,
            lon=BASE_LON - 0.010,
            available=True,
            capacity=6,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.FIRE_RESPONSE_TEAM],
            operating_cost_per_hour=220.0,
            response_speed_kmh=50.0,
        ),
        Resource(
            id="RES-AMB-02",
            name="Paramedic Ambulance Beta (Engine Failure)",
            resource_type=ResourceType.AMBULANCE.value,
            lat=BASE_LAT - 0.020,
            lon=BASE_LON + 0.020,
            available=False,
            capacity=4,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.AMBULANCE],
            operating_cost_per_hour=140.0,
            response_speed_kmh=55.0,
            assignment_status="Unavailable",
        ),
        Resource(
            id="RES-MED-01",
            name="Mobile Medical Unit (Under Maintenance)",
            resource_type=ResourceType.MEDICAL_SUPPLY_UNIT.value,
            lat=BASE_LAT + 0.020,
            lon=BASE_LON - 0.020,
            available=False,
            capacity=12,
            operational_capabilities=RESOURCE_CAPABILITIES[ResourceType.MEDICAL_SUPPLY_UNIT],
            operating_cost_per_hour=110.0,
            response_speed_kmh=48.0,
            assignment_status="Unavailable",
        ),
    ]

    for inc in incidents:
        prioritize_incident(inc)

    return Scenario(
        id="SCENARIO-D",
        name="Scenario D: Resource Shortage Emergency",
        description="Severe resource-constrained event with 6 competing high-priority incidents and only 3 operational units, forcing strict mathematical trade-offs.",
        scenario_type="Resource Shortage",
        incidents=incidents,
        resources=resources,
        road_congestion_factor=1.75,
        weather_impact="Active storm & gridlock",
        random_seed=404,
    )


def generate_custom_scenario(
    n_incidents: int = 5,
    n_resources: int = 5,
    scenario_name: str = "Custom Disaster Simulation",
    random_seed: int = 42,
) -> Scenario:
    """
    Dynamically generates a balanced, realistic synthetic scenario with deterministic seed.
    """
    rng = random.Random(random_seed)
    
    categories = list(DisasterCategory)
    resource_types = list(ResourceType)
    
    incidents: List[Incident] = []
    for i in range(n_incidents):
        cat = rng.choice(categories).value
        # Pick 1 or 2 required resource types
        if cat in [DisasterCategory.FIRE.value]:
            reqs = [ResourceType.FIRE_RESPONSE_TEAM.value]
            if rng.random() > 0.4:
                reqs.append(ResourceType.AMBULANCE.value)
        elif cat in [DisasterCategory.BUILDING_COLLAPSE.value, DisasterCategory.LANDSLIDE.value]:
            reqs = [ResourceType.RESCUE_TEAM.value]
            if rng.random() > 0.3:
                reqs.append(ResourceType.AMBULANCE.value)
        elif cat == DisasterCategory.MEDICAL_EMERGENCY.value:
            reqs = [ResourceType.AMBULANCE.value]
        else:
            reqs = [rng.choice(resource_types).value]
            
        sev = rng.randint(1, 5)
        people = int(rng.expovariate(1.0 / 30.0)) + 2
        people = min(250, people)
        
        inc = Incident(
            id=f"INC-GEN-{i+1:02d}",
            name=f"{cat} Alert #{i+1}",
            category=cat,
            lat=BASE_LAT + rng.uniform(-0.045, 0.045),
            lon=BASE_LON + rng.uniform(-0.045, 0.045),
            people_affected=people,
            severity=sev,
            required_resource_types=reqs,
            estimated_service_duration=round(rng.uniform(20.0, 70.0), 1),
            time_sensitivity=rng.randint(1, 5),
            access_difficulty=round(rng.uniform(1.0, 2.2), 2),
        )
        prioritize_incident(inc)
        incidents.append(inc)

    resources: List[Resource] = []
    for j in range(n_resources):
        rtype = resource_types[j % len(resource_types)].value
        avail = True if j > 0 else (rng.random() > 0.15)
        res = Resource(
            id=f"RES-GEN-{j+1:02d}",
            name=f"Deployable {rtype} {chr(65 + j)}",
            resource_type=rtype,
            lat=BASE_LAT + rng.uniform(-0.035, 0.035),
            lon=BASE_LON + rng.uniform(-0.035, 0.035),
            available=avail,
            capacity=rng.randint(3, 10),
            operational_capabilities=RESOURCE_CAPABILITIES.get(ResourceType(rtype), ["standard_response"]),
            operating_cost_per_hour=round(rng.uniform(100.0, 220.0), 1),
            response_speed_kmh=round(rng.uniform(45.0, 65.0), 1),
            assignment_status="Available" if avail else "Unavailable",
        )
        resources.append(res)

    return Scenario(
        id=f"SCENARIO-GEN-{random_seed}",
        name=scenario_name,
        description=f"Synthetic procedural disaster scenario with {n_incidents} incidents and {n_resources} units.",
        scenario_type="Procedural Simulation",
        incidents=incidents,
        resources=resources,
        road_congestion_factor=round(rng.uniform(1.1, 1.7), 2),
        weather_impact="Variable local conditions",
        random_seed=random_seed,
    )
