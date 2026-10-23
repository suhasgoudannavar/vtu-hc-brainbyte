"""
AI/ML Incident Prioritization for QRescue.
Provides:
- Mode A: Transparent multi-factor baseline scoring formula with explainability.
- Mode B: Supervised machine learning experiment on synthetic historical data.
"""

from __future__ import annotations
import math
from typing import Dict, Any, Tuple, List, Optional
import numpy as np

from src.data_models import Incident, DisasterCategory, PriorityLevel


CATEGORY_WEIGHTS: Dict[str, float] = {
    DisasterCategory.BUILDING_COLLAPSE.value: 1.00,
    DisasterCategory.LANDSLIDE.value: 0.95,
    DisasterCategory.FIRE.value: 0.90,
    DisasterCategory.FLOOD.value: 0.85,
    DisasterCategory.MEDICAL_EMERGENCY.value: 0.80,
    DisasterCategory.ROAD_ACCIDENT.value: 0.75,
}

DEFAULT_WEIGHTS: Dict[str, float] = {
    "severity": 0.35,
    "people_affected": 0.25,
    "time_sensitivity": 0.20,
    "hazard_category": 0.10,
    "access_difficulty": 0.10,
}


def calculate_priority_score_baseline(
    incident: Incident,
    weights: Optional[Dict[str, float]] = None,
) -> Tuple[float, str, Dict[str, float], str]:
    """
    Mode A: Transparent Multi-Factor Prioritization Formula.
    
    Returns:
        score: float (0.0 - 100.0)
        category: str ("Critical", "High", "Medium", "Low")
        factors: dict of factor contributions
        explanation: readable explanation string
    """
    w = weights or DEFAULT_WEIGHTS
    
    # 1. Severity factor: [1, 5] -> [0.0, 1.0]
    f_sev = (incident.severity - 1.0) / 4.0
    
    # 2. People affected factor: non-linear logarithmic saturation up to ~500 people
    # 0 people -> 0.0, 10 -> ~0.33, 100 -> ~0.67, 500+ -> 1.0
    f_people = min(1.0, math.log10(max(1.0, float(incident.people_affected)) + 1.0) / math.log10(500.0))
    
    # 3. Time sensitivity factor: [1, 5] -> [0.0, 1.0]
    f_time = (incident.time_sensitivity - 1.0) / 4.0
    
    # 4. Hazard category inherent hazard level
    f_hazard = CATEGORY_WEIGHTS.get(incident.category, 0.70)
    
    # 5. Access difficulty factor: [1.0, 3.0] -> [0.0, 1.0]
    f_access = min(1.0, max(0.0, (incident.access_difficulty - 1.0) / 2.0))
    
    # Weighted composite sum in [0.0, 1.0]
    total_weight = sum(w.values())
    composite = (
        w["severity"] * f_sev +
        w["people_affected"] * f_people +
        w["time_sensitivity"] * f_time +
        w["hazard_category"] * f_hazard +
        w["access_difficulty"] * f_access
    ) / total_weight
    
    score = round(composite * 100.0, 2)
    
    # Determine Priority Category
    if score >= 75.0:
        cat = PriorityLevel.CRITICAL.value
    elif score >= 50.0:
        cat = PriorityLevel.HIGH.value
    elif score >= 30.0:
        cat = PriorityLevel.MEDIUM.value
    else:
        cat = PriorityLevel.LOW.value
        
    factors = {
        "severity_contribution": round(w["severity"] * f_sev * 100.0 / total_weight, 2),
        "people_contribution": round(w["people_affected"] * f_people * 100.0 / total_weight, 2),
        "time_sensitivity_contribution": round(w["time_sensitivity"] * f_time * 100.0 / total_weight, 2),
        "hazard_category_contribution": round(w["hazard_category"] * f_hazard * 100.0 / total_weight, 2),
        "access_difficulty_contribution": round(w["access_difficulty"] * f_access * 100.0 / total_weight, 2),
    }
    
    explanation = (
        f"Simulated Score: {score}/100 ({cat}). "
        f"Driven primarily by Severity lvl {incident.severity}/5 ({factors['severity_contribution']} pts) "
        f"and {incident.people_affected} affected individuals ({factors['people_contribution']} pts)."
    )
    
    return score, cat, factors, explanation


def prioritize_incident(incident: Incident, weights: Optional[Dict[str, float]] = None) -> Incident:
    """Updates the incident in-place with baseline prioritization."""
    score, cat, factors, explanation = calculate_priority_score_baseline(incident, weights)
    incident.urgency_score = score
    incident.priority_category = cat
    incident.priority_factors = factors
    incident.priority_explanation = explanation
    return incident


class MLPrioritizationModel:
    """
    Mode B: Optional Machine Learning Prioritization Experiment.
    Trained on reproducible synthetic historical disaster data.
    """

    def __init__(self, random_seed: int = 42):
        self.random_seed = random_seed
        self.model = None
        self.is_trained = False
        self.feature_names = [
            "severity",
            "people_affected",
            "time_sensitivity",
            "category_hazard_index",
            "access_difficulty",
            "estimated_service_duration",
        ]
        self.metrics: Dict[str, Any] = {}
        self.feature_importances: Dict[str, float] = {}

    def generate_synthetic_training_data(self, n_samples: int = 600) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generates realistic synthetic historical triage logs.
        Data labels: 0=Low, 1=Medium, 2=High, 3=Critical.
        Ground truth simulates historical dispatch decisions based on combined risk.
        """
        rng = np.random.default_rng(self.random_seed)
        
        severities = rng.integers(1, 6, size=n_samples)
        people = rng.geometric(p=0.03, size=n_samples)  # skewed positive distribution
        people = np.clip(people, 1, 350)
        time_sens = rng.integers(1, 6, size=n_samples)
        
        category_indices = rng.choice(
            [0.75, 0.80, 0.85, 0.90, 0.95, 1.00],
            size=n_samples,
            p=[0.20, 0.20, 0.20, 0.15, 0.15, 0.10],
        )
        access_diff = rng.uniform(1.0, 2.5, size=n_samples)
        duration = rng.uniform(15.0, 120.0, size=n_samples)
        
        X = np.column_stack([
            severities,
            people,
            time_sens,
            category_indices,
            access_diff,
            duration,
        ])
        
        # Synthetic ground truth triage rule with some real-world noise
        raw_urgency = (
            0.35 * (severities / 5.0) +
            0.30 * np.minimum(1.0, np.log10(people + 1) / 2.5) +
            0.20 * (time_sens / 5.0) +
            0.15 * category_indices
        )
        # Add slight observational noise
        noise = rng.normal(0.0, 0.05, size=n_samples)
        noisy_urgency = np.clip(raw_urgency + noise, 0.0, 1.0)
        
        # Discretize into classes: 0: Low (<0.35), 1: Medium (0.35-0.60), 2: High (0.60-0.80), 3: Critical (>=0.80)
        y = np.zeros(n_samples, dtype=int)
        y[noisy_urgency >= 0.35] = 1
        y[noisy_urgency >= 0.60] = 2
        y[noisy_urgency >= 0.80] = 3
        
        return X, y

    def train(self, n_samples: int = 600) -> Dict[str, Any]:
        """Trains a Scikit-Learn Random Forest Classifier and records evaluation metrics."""
        from sklearn.ensemble import RandomForestClassifier
        from sklearn.model_selection import train_test_split
        from sklearn.metrics import accuracy_score, precision_recall_fscore_support
        
        X, y = self.generate_synthetic_training_data(n_samples=n_samples)
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.20, random_state=self.random_seed, stratify=y
        )
        
        self.model = RandomForestClassifier(
            n_estimators=60,
            max_depth=5,
            random_state=self.random_seed,
        )
        self.model.fit(X_train, y_train)
        
        y_pred = self.model.predict(X_test)
        acc = float(accuracy_score(y_test, y_pred))
        precision, recall, f1, _ = precision_recall_fscore_support(
            y_test, y_pred, average="weighted", zero_division=0
        )
        
        self.metrics = {
            "accuracy": round(acc, 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "n_train": len(X_train),
            "n_test": len(X_test),
            "note": "Evaluation on synthetic simulated historical dispatch records. Not validated clinical triage.",
        }
        
        importances = self.model.feature_importances_
        self.feature_importances = {
            name: round(float(imp), 4)
            for name, imp in zip(self.feature_names, importances)
        }
        self.is_trained = True
        return self.metrics

    def predict_incident(self, incident: Incident) -> Tuple[str, Dict[str, float]]:
        """Predicts priority class and probabilities for a given incident."""
        if not self.is_trained:
            self.train()
            
        cat_index = CATEGORY_WEIGHTS.get(incident.category, 0.70)
        x_vec = np.array([[
            incident.severity,
            incident.people_affected,
            incident.time_sensitivity,
            cat_index,
            incident.access_difficulty,
            incident.estimated_service_duration,
        ]])
        
        pred_class_idx = int(self.model.predict(x_vec)[0])
        class_names = [PriorityLevel.LOW.value, PriorityLevel.MEDIUM.value, PriorityLevel.HIGH.value, PriorityLevel.CRITICAL.value]
        predicted_category = class_names[pred_class_idx]
        
        probs = self.model.predict_proba(x_vec)[0]
        prob_dict = {
            cls_name: round(float(prob), 4)
            for cls_name, prob in zip(class_names[:len(probs)], probs)
        }
        return predicted_category, prob_dict
