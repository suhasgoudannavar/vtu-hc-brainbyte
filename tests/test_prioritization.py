"""
Unit tests for Incident Prioritization (Mode A baseline and Mode B ML model).
"""

import pytest
from src.data_models import Incident, DisasterCategory, ResourceType
from src.prioritization import (
    calculate_priority_score_baseline,
    prioritize_incident,
    MLPrioritizationModel,
)


def test_baseline_priority_ranking():
    # Low severity, few people, low time sensitivity
    inc_low = Incident(
        id="INC-LOW",
        name="Minor road scrape",
        category=DisasterCategory.ROAD_ACCIDENT.value,
        lat=37.77,
        lon=-122.41,
        people_affected=1,
        severity=1,
        time_sensitivity=1,
        access_difficulty=1.0,
    )
    score_low, cat_low, factors_low, _ = calculate_priority_score_baseline(inc_low)

    # Severe building collapse with 100 people trapped
    inc_high = Incident(
        id="INC-HIGH",
        name="Major structural collapse",
        category=DisasterCategory.BUILDING_COLLAPSE.value,
        lat=37.77,
        lon=-122.41,
        people_affected=100,
        severity=5,
        time_sensitivity=5,
        access_difficulty=2.2,
    )
    score_high, cat_high, factors_high, _ = calculate_priority_score_baseline(inc_high)

    assert score_high > score_low
    assert score_high >= 75.0
    assert cat_high in ["Critical", "High"]
    assert cat_low in ["Low", "Medium"]
    assert "severity_contribution" in factors_high


def test_prioritize_incident_in_place():
    inc = Incident(
        id="INC-01",
        name="Flash flood apartment",
        category=DisasterCategory.FLOOD.value,
        lat=37.77,
        lon=-122.41,
        people_affected=25,
        severity=4,
        time_sensitivity=4,
    )
    prioritize_incident(inc)
    assert inc.urgency_score > 0.0
    assert inc.priority_category in ["Critical", "High", "Medium", "Low"]
    assert len(inc.priority_explanation) > 10


def test_ml_prioritization_training_and_inference():
    ml_model = MLPrioritizationModel(random_seed=42)
    metrics = ml_model.train(n_samples=200)

    assert ml_model.is_trained is True
    assert "accuracy" in metrics
    assert metrics["accuracy"] >= 0.50
    assert "f1_score" in metrics
    assert len(ml_model.feature_importances) == 6

    inc = Incident(
        id="INC-TEST",
        name="Chemical plant fire",
        category=DisasterCategory.FIRE.value,
        lat=37.77,
        lon=-122.41,
        people_affected=40,
        severity=5,
        time_sensitivity=5,
    )
    pred_cat, probs = ml_model.predict_incident(inc)
    assert pred_cat in ["Critical", "High", "Medium", "Low"]
    assert sum(probs.values()) == pytest.approx(1.0, abs=1e-3)
