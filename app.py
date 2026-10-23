"""
QRescue: AI-Powered Disaster Response Using Quantum Optimization.
Operational Decision-Support System for Emergency Operations Centers & Quantum Researchers.

Complete Professional UI Redesign:
- Clean dark navy/charcoal surface styling
- High-contrast typography (Inter & IBM Plex Mono)
- 9 Functional Navigation Sections
- Real-time simulation header bar with quick-run & reset
- 4 Compact KPI Panels with actual calculated metrics
- Full Plotly visualization suite using real data
- Multi-scenario simulator (Flood, Landslide, Multi-Hazard, Resource Shortage, Custom)
- Comprehensive Incident & Resource Management with live availability switchboard
- Scientific Optimization Lab & Quantum QAOA Lab
- Side-by-side multi-algorithm benchmarks & formal report exports
"""

from __future__ import annotations
import copy
import time
from datetime import datetime
from typing import List, Dict, Any, Optional

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_models import (
    Incident,
    Resource,
    Scenario,
    DisasterCategory,
    ResourceType,
    PriorityLevel,
    OptimizationResult,
    RESOURCE_CAPABILITIES,
)
from src.sample_data import (
    get_scenario_urban_flood,
    get_scenario_landslide,
    get_scenario_multihazard,
    get_scenario_resource_shortage,
    generate_custom_scenario,
    BASE_LAT,
    BASE_LON,
)
from src.prioritization import (
    prioritize_incident,
    calculate_priority_score_baseline,
    MLPrioritizationModel,
    DEFAULT_WEIGHTS,
)
from src.response_time import (
    estimate_travel_distance,
    calculate_incident_resource_response,
)
from src.classical_optimizer import (
    run_greedy_baseline,
    run_ortools_optimizer,
    validate_assignments,
)
from src.qubo_model import AllocationQUBO
from src.quantum_optimizer import run_qaoa_optimizer
from src.evaluation import run_full_comparison, calculate_percentage_improvement
from src.reporting import (
    create_experiment_payload,
    export_experiment_json,
    export_experiment_csv_bundle,
    generate_markdown_report,
)
from src.ui_helpers import (
    CUSTOM_CSS,
    render_spatial_simulation_map,
    render_incident_severity_chart,
    render_resource_utilization_chart,
    render_response_time_analysis_chart,
    render_incident_priority_matrix,
    render_comparison_charts,
    render_quantum_distribution_chart,
    render_experiment_history_chart,
)


# ==============================================================================
# Page Configuration & Design System Injection
# ==============================================================================
st.set_page_config(
    page_title="QRescue | AI & Quantum Disaster Response Platform",
    page_icon="🚨",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)


# ==============================================================================
# Session State Initialization
# ==============================================================================
def init_session():
    if "scenario" not in st.session_state:
        st.session_state.scenario = get_scenario_urban_flood()
    if "current_result" not in st.session_state:
        st.session_state.current_result = None
    if "comparison_data" not in st.session_state:
        st.session_state.comparison_data = None
    if "experiment_history" not in st.session_state:
        st.session_state.experiment_history = []
    if "last_calculation_time" not in st.session_state:
        st.session_state.last_calculation_time = "STANDBY"
    if "selected_incident_id" not in st.session_state:
        st.session_state.selected_incident_id = None
    if "selected_resource_id" not in st.session_state:
        st.session_state.selected_resource_id = None
    if "ml_model" not in st.session_state:
        st.session_state.ml_model = MLPrioritizationModel(random_seed=42)
    if "ml_trained" not in st.session_state:
        st.session_state.ml_trained = False

init_session()


def execute_current_simulation(algorithm_name: str = "Classical (Google OR-Tools CP-SAT)"):
    """Executes the selected optimizer and updates global session state."""
    scen: Scenario = st.session_state.scenario
    t0 = time.perf_counter()
    if "OR-Tools" in algorithm_name or "Classical" in algorithm_name:
        res = run_ortools_optimizer(
            incidents=scen.incidents,
            resources=scen.resources,
            congestion_factor=scen.road_congestion_factor,
        )
    elif "Quantum" in algorithm_name or "QAOA" in algorithm_name:
        res = run_qaoa_optimizer(
            incidents=scen.incidents,
            resources=scen.resources,
            congestion_factor=scen.road_congestion_factor,
            p_layers=1,
            shots=512,
            maxiter=15,
        )
    else:
        res = run_greedy_baseline(
            incidents=scen.incidents,
            resources=scen.resources,
            congestion_factor=scen.road_congestion_factor,
        )

    st.session_state.current_result = res
    st.session_state.last_calculation_time = datetime.now().strftime("%H:%M:%S")
    st.session_state.experiment_history.append({
        "timestamp": st.session_state.last_calculation_time,
        "scenario": scen.name,
        "algorithm": res.algorithm_name,
        "status": res.status,
        "served": len(res.served_incident_ids),
        "unserved": len(res.unserved_incident_ids),
        "weighted_time": round(res.total_weighted_response_time, 2),
        "objective": round(res.objective_value, 2),
        "runtime": round(res.runtime_sec, 4),
    })
    return res


# ==============================================================================
# Left Sidebar Navigation Shell
# ==============================================================================
with st.sidebar:
    # 1. Brand Block
    st.markdown(
        """
        <div class="sidebar-brand-box">
            <div class="brand-icon">Q</div>
            <div>
                <div class="brand-title">QRESCUE</div>
                <div class="brand-subtitle">AI + QUANTUM PLATFORM</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Operations Context Callout
    st.markdown(
        """
        <div class="notice-box">
            <strong>OPERATIONAL DISPATCH CONSOLE</strong><br>
            Precision emergency triage, geospatial routing, and exact CP-SAT & QAOA quantum optimization.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 3. Main Application Section Navigation
    st.markdown("#### Navigation")
    nav_page = st.radio(
        "Navigation",
        [
            "Overview",
            "Disaster Scenarios",
            "Incident Management",
            "Resource Management",
            "Optimization Lab",
            "Quantum Lab",
            "Algorithm Comparison",
            "Analytics and Reports",
            "Settings and Methodology",
        ],
        index=0,
        label_visibility="collapsed",
    )

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)

    # 4. Scenario Quick Switcher
    st.markdown("#### Scenario Preset")
    preset_map = {
        "Urban Flood Crisis": "SCENARIO-A",
        "Steep Ridge Landslide": "SCENARIO-B",
        "Multi-Hazard Disaster": "SCENARIO-C",
        "Resource Shortage": "SCENARIO-D",
    }
    
    current_preset_idx = 0
    if st.session_state.scenario.id == "SCENARIO-B":
        current_preset_idx = 1
    elif st.session_state.scenario.id == "SCENARIO-C":
        current_preset_idx = 2
    elif st.session_state.scenario.id == "SCENARIO-D":
        current_preset_idx = 3

    quick_preset = st.selectbox(
        "Active Disaster Scenario",
        list(preset_map.keys()),
        index=current_preset_idx,
    )

    if st.button("Load Preset Scenario", use_container_width=True):
        if quick_preset == "Urban Flood Crisis":
            st.session_state.scenario = get_scenario_urban_flood()
        elif quick_preset == "Steep Ridge Landslide":
            st.session_state.scenario = get_scenario_landslide()
        elif quick_preset == "Multi-Hazard Disaster":
            st.session_state.scenario = get_scenario_multihazard()
        elif quick_preset == "Resource Shortage":
            st.session_state.scenario = get_scenario_resource_shortage()
        st.session_state.current_result = None
        st.session_state.comparison_data = None
        st.session_state.last_calculation_time = "STANDBY"
        st.session_state.selected_incident_id = None
        st.session_state.selected_resource_id = None
        st.rerun()

    # 5. Congestion Multiplier Slider
    st.markdown("#### Road Congestion")
    road_congestion = st.slider(
        "Transit Congestion Factor",
        min_value=1.0,
        max_value=2.5,
        value=float(st.session_state.scenario.road_congestion_factor),
        step=0.1,
        help="Simulates travel delay caused by water inundation, debris, and damaged infrastructure.",
    )
    st.session_state.scenario.road_congestion_factor = road_congestion

    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.caption("Engine: Google OR-Tools CP-SAT | Qiskit Aer | Python 3.12")


# ==============================================================================
# Top Command Header Bar
# ==============================================================================
scen: Scenario = st.session_state.scenario
res_result: Optional[OptimizationResult] = st.session_state.current_result

# Status Pill Logic
if not res_result:
    status_html = '<span class="status-pill status-standby"><span class="status-pill-dot"></span>STANDBY (Pending Dispatch)</span>'
elif res_result.status == "OPTIMAL":
    status_html = f'<span class="status-pill status-optimal"><span class="status-pill-dot"></span>OPTIMAL ({res_result.algorithm_name})</span>'
elif res_result.status == "FEASIBLE":
    status_html = f'<span class="status-pill status-feasible"><span class="status-pill-dot"></span>FEASIBLE ({res_result.algorithm_name})</span>'
else:
    status_html = f'<span class="status-pill status-infeasible"><span class="status-pill-dot"></span>{res_result.status}</span>'

calc_time = st.session_state.last_calculation_time

top_col_header, top_col_btns = st.columns([4, 2])
with top_col_header:
    st.markdown(
        f"""
        <div class="app-shell-header">
            <div class="app-shell-title-group">
                <span class="app-shell-title">QRESCUE MISSION CONTROL</span>
                <span class="app-shell-badge">OPS CENTER</span>
            </div>
            <div class="app-shell-meta">
                <div class="app-shell-meta-item">SCENARIO: <strong>{scen.name.upper()}</strong></div>
                <div class="app-shell-meta-item">STATUS: {status_html}</div>
                <div class="app-shell-meta-item">LAST RUN: <strong>{calc_time}</strong></div>
                <div class="app-shell-meta-item">CONGESTION: <strong>{scen.road_congestion_factor:.2f}x</strong></div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

with top_col_btns:
    b1, b2 = st.columns(2)
    with b1:
        if st.button("▶ Run Simulation", type="primary", use_container_width=True):
            with st.spinner("Executing Google OR-Tools CP-SAT solver..."):
                execute_current_simulation("Classical (Google OR-Tools CP-SAT)")
                st.success("Simulation completed.")
                st.rerun()
    with b2:
        if st.button("↺ Reset Scenario", use_container_width=True):
            if scen.id == "SCENARIO-A":
                st.session_state.scenario = get_scenario_urban_flood()
            elif scen.id == "SCENARIO-B":
                st.session_state.scenario = get_scenario_landslide()
            elif scen.id == "SCENARIO-C":
                st.session_state.scenario = get_scenario_multihazard()
            elif scen.id == "SCENARIO-D":
                st.session_state.scenario = get_scenario_resource_shortage()
            st.session_state.current_result = None
            st.session_state.comparison_data = None
            st.session_state.last_calculation_time = "STANDBY"
            st.session_state.selected_incident_id = None
            st.session_state.selected_resource_id = None
            st.rerun()


# ==============================================================================
# SECTION 1: OVERVIEW DASHBOARD
# ==============================================================================
if nav_page == "Overview":
    st.markdown("## Overview Dashboard")
    st.caption("Live spatial situational awareness, triage severity distribution, and deployable fleet allocation manifest.")

    # 1. Four Compact KPI Panels (Actual Computed Data)
    total_inc = len(scen.incidents)
    avail_res = sum(1 for r in scen.resources if r.available)
    total_res = len(scen.resources)
    offline_res = total_res - avail_res
    crit_count = sum(1 for i in scen.incidents if i.priority_category in ["Critical", "High"])

    if res_result:
        assigned_inc = len(res_result.served_incident_ids)
        unassigned_inc = len(res_result.unserved_incident_ids)
        assigned_pct = (assigned_inc / total_inc * 100.0) if total_inc > 0 else 0
        unserved_sub = f"{unassigned_inc} incident(s) unserved due to capacity limits" if unassigned_inc > 0 else "All emergencies successfully served"
    else:
        assigned_inc = 0
        unassigned_inc = total_inc
        assigned_pct = 0
        unserved_sub = "Awaiting simulation execution"

    st.markdown(
        f"""
        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-accent-bar kpi-accent-red"></div>
                <div class="kpi-header">
                    <span class="kpi-title">Active Incidents</span>
                    <div class="kpi-icon-wrap">🚨</div>
                </div>
                <div class="kpi-value">{total_inc}</div>
                <div class="kpi-subtext"><strong>{crit_count}</strong> Critical / High urgency load</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-accent-bar kpi-accent-green"></div>
                <div class="kpi-header">
                    <span class="kpi-title">Available Resources</span>
                    <div class="kpi-icon-wrap">🛡️</div>
                </div>
                <div class="kpi-value">{avail_res} <span style="font-size:1.1rem;color:#64748B;">/ {total_res}</span></div>
                <div class="kpi-subtext"><strong>{offline_res}</strong> unit(s) offline in maintenance</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-accent-bar kpi-accent-cyan"></div>
                <div class="kpi-header">
                    <span class="kpi-title">Incidents Assigned</span>
                    <div class="kpi-icon-wrap">✓</div>
                </div>
                <div class="kpi-value" style="color:#00E5FF;">{assigned_inc} <span style="font-size:1.1rem;color:#64748B;">({assigned_pct:.0f}%)</span></div>
                <div class="kpi-subtext"><strong>{assigned_inc}</strong> verified capability matches</div>
            </div>
            <div class="kpi-card">
                <div class="kpi-accent-bar kpi-accent-orange"></div>
                <div class="kpi-header">
                    <span class="kpi-title">Incidents Unserved</span>
                    <div class="kpi-icon-wrap">⚠️</div>
                </div>
                <div class="kpi-value" style="color:{'#EF4444' if unassigned_inc > 0 else '#94A3B8'};">{unassigned_inc}</div>
                <div class="kpi-subtext">{unserved_sub}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 2. Main Dashboard Layout: Map & Inspector
    col_map_layout, col_inspector = st.columns([1.85, 1.0])

    with col_map_layout:
        st.markdown("### Disaster Operations Map")
        st.caption("Coordinate visualization (synthetic coordinates, Haversine distance with 1.35x curvature & congestion factor).")

        # Layer controls row
        c_lay1, c_lay2, c_lay3 = st.columns(3)
        with c_lay1:
            lay_inc = st.checkbox("Show Incidents Layer", value=True)
        with c_lay2:
            lay_res = st.checkbox("Show Fleet Assets Layer", value=True)
        with c_lay3:
            lay_rot = st.checkbox("Show Dispatch Vectors", value=True)

        assignments = res_result.assignments if res_result else None
        map_fig = render_spatial_simulation_map(
            incidents=scen.incidents,
            resources=scen.resources,
            assignments=assignments,
            show_incidents=lay_inc,
            show_resources=lay_res,
            show_routes=lay_rot,
            selected_incident_id=st.session_state.selected_incident_id,
            selected_resource_id=st.session_state.selected_resource_id,
        )
        st.plotly_chart(map_fig, use_container_width=True)

    with col_inspector:
        st.markdown("### Detail Inspection Panel")
        st.caption("Select an incident or fleet unit to inspect actual telemetry.")

        insp_type = st.radio("Inspect Target", ["Incident", "Resource"], horizontal=True)

        if insp_type == "Incident":
            inc_options = {f"{i.id} - {i.name}": i.id for i in scen.incidents}
            selected_label = st.selectbox("Select Incident", list(inc_options.keys()))
            sel_inc_id = inc_options[selected_label]
            st.session_state.selected_incident_id = sel_inc_id
            target_inc = next((i for i in scen.incidents if i.id == sel_inc_id), None)

            if target_inc:
                assigned_units = []
                transit_time = "---"
                fulfillment = "UNSERVED"
                if res_result and res_result.assignments:
                    for asgn in res_result.assignments:
                        if asgn.incident_id == target_inc.id:
                            assigned_units = asgn.resource_names
                            transit_time = f"{asgn.estimated_travel_time_min:.1f} min"
                            fulfillment = "FULFILLED" if asgn.is_fully_served else ("PARTIAL" if assigned_units else "UNSERVED")

                badge_class = "badge-critical" if target_inc.priority_category in ["Critical", "High"] else "badge-warning" if target_inc.priority_category == "Medium" else "badge-neutral"

                st.markdown(
                    f"""
                    <div class="surface-panel">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="font-size:0.95rem;">{target_inc.name}</strong>
                            <span class="badge {badge_class}">{target_inc.priority_category}</span>
                        </div>
                        <div class="divider"></div>
                        <div style="font-size:0.80rem;line-height:1.7;font-family:var(--font-mono);">
                            Incident ID: <strong>{target_inc.id}</strong><br>
                            Hazard Category: <strong>{target_inc.category}</strong><br>
                            Severity: <strong>{target_inc.severity}/5</strong> | Time Sens: <strong>{target_inc.time_sensitivity}/5</strong><br>
                            Casualties / At-Risk: <strong>{target_inc.people_affected} persons</strong><br>
                            Priority Score: <strong>{target_inc.urgency_score:.1f} / 100</strong><br>
                            Required Fleet: <strong>{', '.join(target_inc.required_resource_types)}</strong><br>
                            Access Barrier: <strong>{target_inc.access_difficulty:.2f}x</strong><br>
                            Coordinates: <strong>({target_inc.lat:.4f}, {target_inc.lon:.4f})</strong><br>
                            <div class="divider"></div>
                            Dispatch State: <strong style="color:{'#00E5FF' if fulfillment == 'FULFILLED' else ('#F59E0B' if fulfillment == 'PARTIAL' else '#EF4444')};">{fulfillment}</strong><br>
                            Assigned Units: <strong>{', '.join(assigned_units) if assigned_units else 'None'}</strong><br>
                            Transit Delay: <strong>{transit_time}</strong>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        else:
            res_options = {f"{r.id} - {r.name}": r.id for r in scen.resources}
            selected_res_label = st.selectbox("Select Resource", list(res_options.keys()))
            sel_res_id = res_options[selected_res_label]
            st.session_state.selected_resource_id = sel_res_id
            target_res = next((r for r in scen.resources if r.id == sel_res_id), None)

            if target_res:
                assigned_to = "Standby (Unassigned)"
                if res_result and res_result.assignments:
                    for asgn in res_result.assignments:
                        if target_res.id in asgn.resource_ids:
                            assigned_to = f"{asgn.incident_name} [{asgn.incident_id}]"

                badge_res = "badge-success" if target_res.available else "badge-neutral"

                st.markdown(
                    f"""
                    <div class="surface-panel">
                        <div style="display:flex;justify-content:space-between;align-items:center;">
                            <strong style="font-size:0.95rem;">{target_res.name}</strong>
                            <span class="badge {badge_res}">{'OPERATIONAL' if target_res.available else 'MAINTENANCE'}</span>
                        </div>
                        <div class="divider"></div>
                        <div style="font-size:0.80rem;line-height:1.7;font-family:var(--font-mono);">
                            Resource ID: <strong>{target_res.id}</strong><br>
                            Classification: <strong>{target_res.resource_type}</strong><br>
                            Base Coordinates: <strong>({target_res.lat:.4f}, {target_res.lon:.4f})</strong><br>
                            Cruising Speed: <strong>{target_res.response_speed_kmh:.1f} km/h</strong><br>
                            Operating Cost: <strong>${target_res.operating_cost_per_hour:.2f}/hr</strong><br>
                            Transport Capacity: <strong>{target_res.capacity} persons</strong><br>
                            Capabilities: <strong>{', '.join(target_res.operational_capabilities)}</strong><br>
                            <div class="divider"></div>
                            Current Mission: <strong>{assigned_to}</strong>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

    # 3. Operations Analytics Visualizations Row
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### Operational Analytics")

    g_col1, g_col2, g_col3 = st.columns(3)
    with g_col1:
        st.markdown("#### Incident Severity Distribution")
        fig_sev = render_incident_severity_chart(scen.incidents)
        st.plotly_chart(fig_sev, use_container_width=True)

    with g_col2:
        st.markdown("#### Fleet Readiness & Utilization")
        fig_util = render_resource_utilization_chart(scen.resources, assignments)
        st.plotly_chart(fig_util, use_container_width=True)

    with g_col3:
        st.markdown("#### Estimated Response-Time Delay")
        fig_resp = render_response_time_analysis_chart(assignments or [], scen.incidents)
        st.plotly_chart(fig_resp, use_container_width=True)

    # 4. Resource Assignment Status Manifest & Bottleneck Explanation
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### Resource Assignment Status & Manifest")

    if res_result and res_result.assignments:
        manifest_rows = []
        for asgn in res_result.assignments:
            manifest_rows.append({
                "Incident ID": asgn.incident_id,
                "Incident Location": asgn.incident_name,
                "Assigned Resource Units": "; ".join(asgn.resource_names) if asgn.resource_names else "[UNASSIGNED]",
                "Transit Time (min)": f"{asgn.estimated_travel_time_min:.1f}" if asgn.resource_names else "---",
                "Total Service Duration (min)": f"{asgn.total_response_time_min:.1f}" if asgn.resource_names else "---",
                "Operating Cost ($)": f"${asgn.operating_cost:.2f}",
                "Fulfillment Status": "FULFILLED" if asgn.is_fully_served else ("PARTIAL" if asgn.resource_names else "UNSERVED"),
                "Unmet Capability Types": "; ".join(asgn.missing_resource_types) if asgn.missing_resource_types else "None",
            })
        st.dataframe(pd.DataFrame(manifest_rows), use_container_width=True, hide_index=True)

        # Bottleneck Diagnostics
        unserved_list = [a for a in res_result.assignments if not a.is_fully_served]
        if unserved_list:
            reasons = []
            for u in unserved_list:
                missing = ", ".join(u.missing_resource_types) if u.missing_resource_types else "No available unit"
                reasons.append(f"**{u.incident_id} ({u.incident_name}):** Missing `{missing}` due to fleet allocation prioritizing higher urgency emergencies.")
            
            st.markdown(
                f"""
                <div class="notice-box">
                    <strong>BOTTLENECK EXPLANATION: WHY CERTAIN EMERGENCIES REMAIN UNSERVED</strong><br>
                    {'<br>'.join(reasons)}
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.info("No active optimization run. Click 'Run Simulation' in the header to execute the allocation solver.")


# ==============================================================================
# SECTION 2: DISASTER SCENARIOS
# ==============================================================================
elif nav_page == "Disaster Scenarios":
    st.markdown("## Disaster Scenario Simulator")
    st.caption("Configure simulated emergency parameters, select benchmark presets, or procedurally generate custom disaster events.")

    # 1. Preset Scenarios Section
    st.markdown("### Scenario Presets")
    sc_c1, sc_c2 = st.columns([1.2, 1])

    with sc_c1:
        preset_choice = st.radio(
            "Select Disaster Preset",
            [
                "Scenario A: Urban Flood Crisis",
                "Scenario B: Steep Ridge Landslide",
                "Scenario C: Multi-Hazard Urban Disaster",
                "Scenario D: Resource Shortage Emergency",
                "Scenario E: Custom Procedural Generator",
            ],
            index=0 if scen.id == "SCENARIO-A" else (1 if scen.id == "SCENARIO-B" else (2 if scen.id == "SCENARIO-C" else (3 if scen.id == "SCENARIO-D" else 4))),
        )

        if st.button("Apply Selected Preset", use_container_width=True, type="primary"):
            if "Urban Flood" in preset_choice:
                st.session_state.scenario = get_scenario_urban_flood()
            elif "Landslide" in preset_choice:
                st.session_state.scenario = get_scenario_landslide()
            elif "Multi-Hazard" in preset_choice:
                st.session_state.scenario = get_scenario_multihazard()
            elif "Resource Shortage" in preset_choice:
                st.session_state.scenario = get_scenario_resource_shortage()
            st.session_state.current_result = None
            st.session_state.comparison_data = None
            st.session_state.last_calculation_time = "STANDBY"
            st.session_state.selected_incident_id = None
            st.session_state.selected_resource_id = None
            st.success("Scenario preset loaded.")
            st.rerun()

    with sc_c2:
        st.markdown(
            f"""
            <div class="surface-panel">
                <strong style="font-size:0.95rem;color:var(--accent-cyan);">{scen.name}</strong>
                <div class="divider"></div>
                <div style="font-size:0.82rem;line-height:1.7;font-family:var(--font-mono);">
                    Scenario Type: <strong>{scen.scenario_type}</strong><br>
                    Incidents Count: <strong>{len(scen.incidents)}</strong><br>
                    Total Fleet Assets: <strong>{len(scen.resources)}</strong><br>
                    Operational Assets: <strong>{sum(1 for r in scen.resources if r.available)}</strong><br>
                    Road Congestion Multiplier: <strong>{scen.road_congestion_factor:.2f}x</strong><br>
                    Environmental Impact: <strong>{scen.weather_impact}</strong><br>
                    Description: <em>{scen.description}</em>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Custom Scenario Generator
    if "Custom Procedural Generator" in preset_choice or "GEN" in scen.id:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### Custom Procedural Scenario Generator")
        with st.form("custom_scenario_form"):
            cf_c1, cf_c2, cf_c3 = st.columns(3)
            with cf_c1:
                gen_incidents = st.slider("Number of Incidents", 3, 12, 6)
                gen_ambulances = st.slider("Ambulance Units", 1, 5, 2)
            with cf_c2:
                gen_rescues = st.slider("Rescue Teams", 1, 5, 2)
                gen_fire = st.slider("Fire Response Teams", 0, 4, 1)
            with cf_c3:
                gen_medical = st.slider("Medical Supply Depots", 0, 4, 1)
                gen_seed = st.number_input("Procedural Seed", 1, 99999, 42)

            gen_congestion = st.slider("Simulated Transit Congestion", 1.0, 2.5, 1.4, 0.1)

            if st.form_submit_button("Generate Procedural Scenario"):
                total_units = gen_ambulances + gen_rescues + gen_fire + gen_medical
                new_scen = generate_custom_scenario(
                    n_incidents=gen_incidents,
                    n_resources=total_units,
                    scenario_name=f"Custom Procedural Scenario (Seed {gen_seed})",
                    random_seed=int(gen_seed),
                )
                new_scen.road_congestion_factor = gen_congestion
                st.session_state.scenario = new_scen
                st.session_state.current_result = None
                st.session_state.comparison_data = None
                st.session_state.last_calculation_time = "STANDBY"
                st.success(f"Procedural scenario generated with {gen_incidents} incidents and {total_units} units.")
                st.rerun()

    # 3. Simulation Execution Trigger
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### Run Simulation on Current Scenario")
    st.caption("Validates scenario inputs, runs Google OR-Tools CP-SAT exact optimizer, and updates all telemetry.")

    if st.button("Execute Simulation on Scenario", type="primary", use_container_width=True):
        with st.spinner("Validating constraints and solving allocation problem via CP-SAT..."):
            res = execute_current_simulation("Classical (Google OR-Tools CP-SAT)")
            st.success(f"Simulation completed in {res.runtime_sec:.4f}s with status {res.status}.")
            st.rerun()


# ==============================================================================
# SECTION 3: INCIDENT MANAGEMENT TABLE
# ==============================================================================
elif nav_page == "Incident Management":
    st.markdown("## Incident Management Registry")
    st.caption("Comprehensive registry of all simulated emergencies. Filter, inspect, register, update, and manage incidents.")

    # Controls: Search and Filters
    c_srch, c_cat, c_sev, c_stat = st.columns([1.5, 1, 1, 1])
    with c_srch:
        search_query = st.text_input("Search Incidents (ID, Name, or Description)", "")
    with c_cat:
        cat_filter = st.selectbox("Hazard Category", ["All Categories"] + [c.value for c in DisasterCategory])
    with c_sev:
        sev_filter = st.selectbox("Severity Level", ["All Levels", "5 (Critical)", "4 (High)", "3 (Moderate)", "2 (Minor)", "1 (Routine)"])
    with c_stat:
        status_filter = st.selectbox("Assignment Status", ["All Statuses", "Fulfilled", "Partial", "Unassigned"])

    # Filter incidents
    filtered_incidents = scen.incidents
    if search_query:
        q = search_query.lower()
        filtered_incidents = [i for i in filtered_incidents if q in i.id.lower() or q in i.name.lower()]
    if cat_filter != "All Categories":
        filtered_incidents = [i for i in filtered_incidents if i.category == cat_filter]
    if sev_filter != "All Levels":
        target_sev = int(sev_filter.split()[0])
        filtered_incidents = [i for i in filtered_incidents if i.severity == target_sev]

    # Incident Table
    table_data = []
    for inc in filtered_incidents:
        asgn_status = "UNASSIGNED"
        transit_str = "---"
        assigned_units_str = "None"
        if res_result and res_result.assignments:
            match = next((a for a in res_result.assignments if a.incident_id == inc.id), None)
            if match:
                asgn_status = "FULFILLED" if match.is_fully_served else ("PARTIAL" if match.resource_ids else "UNASSIGNED")
                if match.resource_names:
                    assigned_units_str = "; ".join(match.resource_names)
                    transit_str = f"{match.estimated_travel_time_min:.1f} min"

        if status_filter != "All Statuses" and asgn_status != status_filter.upper():
            continue

        table_data.append({
            "Incident ID": inc.id,
            "Incident Name": inc.name,
            "Category": inc.category,
            "Severity": f"{inc.severity}/5",
            "Casualties": inc.people_affected,
            "Priority Score": f"{inc.urgency_score:.1f}",
            "Triage Priority": inc.priority_category.upper(),
            "Required Assets": "; ".join(inc.required_resource_types),
            "Service Time": f"{inc.estimated_service_duration:.0f} min",
            "Access Barrier": f"{inc.access_difficulty:.2f}x",
            "Status": asgn_status,
            "Assigned Units": assigned_units_str,
            "Transit Time": transit_str,
        })

    if table_data:
        st.dataframe(pd.DataFrame(table_data), use_container_width=True, hide_index=True)
    else:
        st.info("No incidents match the active search and filter criteria.")

    # Actions: Register, Edit, Delete
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    t_add, t_edit, t_del = st.tabs(["Register New Incident", "Edit Incident", "Remove Incident"])

    with t_add:
        with st.form("create_incident_form"):
            a_c1, a_c2 = st.columns(2)
            with a_c1:
                n_id = st.text_input("Incident Identifier", f"INC-CUSTOM-{len(scen.incidents)+1:02d}")
                n_name = st.text_input("Event Description", "Critical Tunnel Inundation and Trapped Commuters")
                n_cat = st.selectbox("Hazard Category", [c.value for c in DisasterCategory])
                n_peo = st.number_input("Casualties / Affected Persons", 1, 1000, 25)
                n_sev = st.slider("Severity Level (1-5)", 1, 5, 4)
            with a_c2:
                n_lat = st.number_input("Latitude", 37.0, 39.0, BASE_LAT + 0.012, format="%.4f")
                n_lon = st.number_input("Longitude", -123.0, -121.0, BASE_LON - 0.015, format="%.4f")
                n_time = st.slider("Time Sensitivity (1-5)", 1, 5, 4)
                n_acc = st.slider("Access Barrier (1.0x - 3.0x)", 1.0, 3.0, 1.4, 0.1)
                n_dur = st.number_input("Service Duration (minutes)", 10.0, 240.0, 45.0, 5.0)
                n_req = st.multiselect("Required Unit Types", [t.value for t in ResourceType], default=[ResourceType.AMBULANCE.value])

            if st.form_submit_button("Submit Incident to Registry"):
                new_inc = Incident(
                    id=n_id,
                    name=n_name,
                    category=n_cat,
                    lat=n_lat,
                    lon=n_lon,
                    people_affected=n_peo,
                    severity=n_sev,
                    required_resource_types=n_req,
                    estimated_service_duration=n_dur,
                    time_sensitivity=n_time,
                    access_difficulty=n_acc,
                )
                prioritize_incident(new_inc)
                errs = new_inc.validate()
                if errs:
                    for e in errs:
                        st.error(e)
                else:
                    scen.incidents.append(new_inc)
                    st.session_state.current_result = None
                    st.session_state.comparison_data = None
                    st.success(f"Incident {n_id} ({n_name}) registered in active scenario.")
                    st.rerun()

    with t_edit:
        if scen.incidents:
            edit_options = {f"{i.id} - {i.name}": i.id for i in scen.incidents}
            edit_sel = st.selectbox("Select Incident to Edit", list(edit_options.keys()))
            inc_to_edit = next(i for i in scen.incidents if i.id == edit_options[edit_sel])

            with st.form("edit_incident_form"):
                e_c1, e_c2 = st.columns(2)
                with e_c1:
                    e_name = st.text_input("Name", inc_to_edit.name)
                    e_peo = st.number_input("Casualties", 1, 1000, inc_to_edit.people_affected)
                    e_sev = st.slider("Severity", 1, 5, inc_to_edit.severity)
                with e_c2:
                    e_time = st.slider("Time Sensitivity", 1, 5, inc_to_edit.time_sensitivity)
                    e_acc = st.slider("Access Barrier", 1.0, 3.0, float(inc_to_edit.access_difficulty), 0.1)
                    e_dur = st.number_input("Duration (min)", 10.0, 240.0, float(inc_to_edit.estimated_service_duration), 5.0)

                if st.form_submit_button("Save Incident Modifications"):
                    inc_to_edit.name = e_name
                    inc_to_edit.people_affected = e_peo
                    inc_to_edit.severity = e_sev
                    inc_to_edit.time_sensitivity = e_time
                    inc_to_edit.access_difficulty = e_acc
                    inc_to_edit.estimated_service_duration = e_dur
                    prioritize_incident(inc_to_edit)
                    st.session_state.current_result = None
                    st.session_state.comparison_data = None
                    st.success(f"Incident {inc_to_edit.id} updated.")
                    st.rerun()

    with t_del:
        if len(scen.incidents) > 1:
            del_options = {f"{i.id} - {i.name}": i.id for i in scen.incidents}
            del_sel = st.selectbox("Select Incident to Delete", list(del_options.keys()))
            inc_to_delete = edit_options[del_sel]

            st.warning(f"Confirm deletion of {del_sel}. This removes the emergency from the scenario.")
            confirm_del = st.checkbox("Confirm Deletion Request", key="confirm_del_inc")
            if st.button("Delete Incident", disabled=not confirm_del):
                scen.incidents = [i for i in scen.incidents if i.id != inc_to_delete]
                st.session_state.current_result = None
                st.session_state.comparison_data = None
                st.success(f"Incident {inc_to_delete} removed from scenario.")
                st.rerun()
        else:
            st.info("Scenario must contain at least one active incident.")


# ==============================================================================
# SECTION 4: RESOURCE MANAGEMENT
# ==============================================================================
elif nav_page == "Resource Management":
    st.markdown("## Resource Management")
    st.caption("Fleet asset readiness, capability mapping, speed ratings, and availability management.")

    # Filter controls
    r_f1, r_f2 = st.columns(2)
    with r_f1:
        type_filter = st.selectbox("Filter Classification", ["All Classifications"] + [t.value for t in ResourceType])
    with r_f2:
        avail_filter = st.selectbox("Filter Operational Readiness", ["All Readiness States", "Operational (Available)", "Offline / Maintenance"])

    filtered_resources = scen.resources
    if type_filter != "All Classifications":
        filtered_resources = [r for r in filtered_resources if r.resource_type == type_filter]
    if avail_filter == "Operational (Available)":
        filtered_resources = [r for r in filtered_resources if r.available]
    elif avail_filter == "Offline / Maintenance":
        filtered_resources = [r for r in filtered_resources if not r.available]

    res_table_data = []
    for r in filtered_resources:
        mission_status = "STANDBY"
        if res_result and res_result.assignments:
            for asgn in res_result.assignments:
                if r.id in asgn.resource_ids:
                    mission_status = f"DISPATCHED [{asgn.incident_id}]"

        res_table_data.append({
            "Resource ID": r.id,
            "Asset Designation": r.name,
            "Classification": r.resource_type,
            "Readiness State": "AVAILABLE" if r.available else "OFFLINE",
            "Capacity": f"{r.capacity} persons",
            "Speed": f"{r.response_speed_kmh:.1f} km/h",
            "Operating Cost": f"${r.operating_cost_per_hour:.2f}/hr",
            "Base Coordinates": f"({r.lat:.4f}, {r.lon:.4f})",
            "Mission Assignment": mission_status,
            "Capabilities": "; ".join(r.operational_capabilities[:2]),
        })

    st.dataframe(pd.DataFrame(res_table_data), use_container_width=True, hide_index=True)

    # Availability Switchboard
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### Operational Readiness Switchboard")
    st.caption("Toggle vehicle maintenance status. Inactive vehicles are strictly excluded from assignment by the optimizer.")

    cols_switch = st.columns(3)
    for idx, r in enumerate(scen.resources):
        with cols_switch[idx % 3]:
            st.markdown(f"**{r.id}** — {r.name}")
            toggled = st.toggle(
                f"Readiness: {'Operational' if r.available else 'Offline'}",
                value=r.available,
                key=f"sw_avail_{r.id}",
            )
            if toggled != r.available:
                r.available = toggled
                r.assignment_status = "Available" if toggled else "Unavailable"
                st.session_state.current_result = None
                st.session_state.comparison_data = None
                st.rerun()

    # Commission New Asset Form
    with st.expander("Commission New Fleet Asset", expanded=False):
        with st.form("create_resource_form"):
            rc1, rc2 = st.columns(2)
            with rc1:
                nr_id = st.text_input("Resource Identifier", f"RES-FLEET-{len(scen.resources)+1:02d}")
                nr_name = st.text_input("Unit Designation", "Heavy Extrication Squad Delta")
                nr_type = st.selectbox("Classification", [t.value for t in ResourceType])
                nr_cap = st.number_input("Transport / Evacuation Capacity", 1, 30, 6)
            with rc2:
                nr_lat = st.number_input("Station Latitude", 37.0, 39.0, BASE_LAT, format="%.4f")
                nr_lon = st.number_input("Station Longitude", -123.0, -121.0, BASE_LON, format="%.4f")
                nr_speed = st.number_input("Cruising Speed (km/h)", 20.0, 100.0, 52.0)
                nr_cost = st.number_input("Operating Cost ($/hr)", 50.0, 500.0, 175.0)

            if st.form_submit_button("Commission Asset"):
                new_res = Resource(
                    id=nr_id,
                    name=nr_name,
                    resource_type=nr_type,
                    lat=nr_lat,
                    lon=nr_lon,
                    available=True,
                    capacity=nr_cap,
                    operational_capabilities=RESOURCE_CAPABILITIES.get(ResourceType(nr_type), ["standard_response"]),
                    operating_cost_per_hour=nr_cost,
                    response_speed_kmh=nr_speed,
                )
                errs = new_res.validate()
                if errs:
                    for e in errs:
                        st.error(e)
                else:
                    scen.resources.append(new_res)
                    st.session_state.current_result = None
                    st.session_state.comparison_data = None
                    st.success(f"Asset {nr_id} ({nr_name}) commissioned into fleet.")
                    st.rerun()


# ==============================================================================
# SECTION 5: OPTIMIZATION LAB
# ==============================================================================
elif nav_page == "Optimization Lab":
    st.markdown("## Optimization Lab")
    st.caption("Configure multi-objective constraints, choose optimization solvers, and execute mathematical resource dispatch.")

    # Algorithm Selection & Objective Tuning
    c_cfg1, c_cfg2 = st.columns([1.2, 1])

    with c_cfg1:
        st.markdown("### 1. Solver Selection")
        selected_engine = st.selectbox(
            "Optimization Solver Engine",
            [
                "Classical (Google OR-Tools CP-SAT)",
                "Quantum (QAOA - Qiskit Aer Simulation)",
                "Greedy Baseline Heuristic",
            ],
            index=0,
        )

        if "Quantum" in selected_engine:
            st.markdown(
                """
                <div class="notice-box">
                    <strong>QAOA QUANTUM SIMULATION (QISKIT AER)</strong><br>
                    Compiles allocation constraints into a QUBO and simulates an Ising Hamiltonian on local classical CPU.
                </div>
                """,
                unsafe_allow_html=True,
            )
            q_layers = st.slider("Ansatz Layers (p)", 1, 3, 1)
            q_shots = st.select_slider("Measurement Shots", [128, 256, 512, 1024, 2048], value=512)
            q_maxiter = st.slider("COBYLA Max Iterations", 5, 40, 15)
            q_sim_seed = st.number_input("Simulation Seed", 1, 9999, 42)

    with c_cfg2:
        st.markdown("### 2. Multi-Objective Weights")
        w_time_val = st.slider("Response Delay Minimization Weight", 0.1, 3.0, 1.0, 0.1)
        w_unserved_val = st.slider("Unserved Priority Penalty Weight", 5.0, 30.0, 15.0, 1.0)
        w_cost_val = st.slider("Resource Operating Cost Weight", 0.01, 0.20, 0.05, 0.01)

    # Primary Action
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    if st.button("Execute Allocation Solver", use_container_width=True, type="primary"):
        with st.spinner(f"Computing allocation plan via {selected_engine}..."):
            t0 = time.perf_counter()
            if "OR-Tools" in selected_engine:
                res = run_ortools_optimizer(
                    incidents=scen.incidents,
                    resources=scen.resources,
                    congestion_factor=scen.road_congestion_factor,
                    weight_response_time=w_time_val,
                    weight_unserved_penalty=w_unserved_val,
                    weight_cost=w_cost_val,
                )
            elif "Quantum" in selected_engine:
                res = run_qaoa_optimizer(
                    incidents=scen.incidents,
                    resources=scen.resources,
                    congestion_factor=scen.road_congestion_factor,
                    p_layers=q_layers,
                    shots=q_shots,
                    maxiter=q_maxiter,
                    random_seed=int(q_sim_seed),
                )
            else:
                res = run_greedy_baseline(
                    incidents=scen.incidents,
                    resources=scen.resources,
                    congestion_factor=scen.road_congestion_factor,
                )

            st.session_state.current_result = res
            st.session_state.last_calculation_time = datetime.now().strftime("%H:%M:%S")

            st.session_state.experiment_history.append({
                "timestamp": st.session_state.last_calculation_time,
                "scenario": scen.name,
                "algorithm": res.algorithm_name,
                "status": res.status,
                "served": len(res.served_incident_ids),
                "unserved": len(res.unserved_incident_ids),
                "weighted_time": round(res.total_weighted_response_time, 2),
                "objective": round(res.objective_value, 2),
                "runtime": round(res.runtime_sec, 4),
            })
            st.success(f"Solver completed in {res.runtime_sec:.4f} seconds.")

    # Results Display
    if st.session_state.current_result:
        res: OptimizationResult = st.session_state.current_result
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown(f"### Solver Results: {res.algorithm_name}")

        r1, r2, r3, r4, r5 = st.columns(5)
        with r1:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Status</div>
                    <div class="kpi-value" style="font-size:1.25rem;">{res.status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with r2:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Served Incidents</div>
                    <div class="kpi-value">{len(res.served_incident_ids)} <span style="font-size:1.0rem;color:#64748B;">/ {len(scen.incidents)}</span></div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with r3:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Weighted Transit</div>
                    <div class="kpi-value" style="font-size:1.25rem;">{res.total_weighted_response_time:.1f}m</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with r4:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Objective Score</div>
                    <div class="kpi-value" style="font-size:1.25rem;">{res.objective_value:.2f}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        with r5:
            st.markdown(
                f"""
                <div class="kpi-card">
                    <div class="kpi-title">Runtime</div>
                    <div class="kpi-value" style="font-size:1.25rem;">{res.runtime_sec:.4f}s</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Constraint Validation Audit
        if not res.is_feasible:
            st.markdown(
                f"""
                <div class="surface-panel" style="border-left:3px solid var(--critical);">
                    <strong style="color:var(--critical);">CONSTRAINT VIOLATIONS DETECTED ({len(res.constraint_violations)}):</strong>
                    <ul style="margin-top:6px;font-size:0.82rem;color:var(--text-secondary);">
                        {''.join(f'<li>{v}</li>' for v in res.constraint_violations)}
                    </ul>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div class="surface-panel" style="border-left:3px solid var(--success);">
                    <strong style="color:var(--success);">UNIVERSAL CONSTRAINT FEASIBILITY CONFIRMED:</strong>
                    <span style="font-size:0.82rem;color:var(--text-secondary);margin-left:6px;">Zero exclusivity conflicts. Strict capability matching. No offline vehicles dispatched.</span>
                </div>
                """,
                unsafe_allow_html=True,
            )


# ==============================================================================
# SECTION 6: QUANTUM LAB
# ==============================================================================
elif nav_page == "Quantum Lab":
    st.markdown("## Quantum Optimization Lab")
    st.caption("Scientific investigation of Quadratic Unconstrained Binary Optimization (QUBO) and Quantum Approximate Optimization Algorithm (QAOA).")

    st.markdown(
        """
        <div class="notice-box">
            <strong>DISCLOSURE: QUANTUM CIRCUIT SIMULATION (CLASSICAL CPU)</strong><br>
            This experiment simulates the Quantum Approximate Optimization Algorithm (QAOA) using <strong>Qiskit Aer</strong> on local CPU.
            Measured runtimes include classical statevector simulation overhead and do not establish physical quantum processor execution or speedup.
        </div>
        """,
        unsafe_allow_html=True,
    )

    # 1. Formulation & Variables Breakdown
    n_inc_q = len(scen.incidents)
    n_res_q = len(scen.resources)
    total_vars = n_inc_q * n_res_q

    q_col1, q_col2 = st.columns([1.2, 1])
    with q_col1:
        st.markdown("### Problem Formulation")
        st.markdown(
            r"""
            **Binary Decision Variables:**
            $$x_{i, r} \in \{0, 1\} \quad \text{for incident } i \in \mathcal{I}, \text{ resource } r \in \mathcal{R}$$

            **QUBO Cost Function:**
            $$H(x) = H_{\text{transit}} - H_{\text{urgency}} + P_{\text{excl}} \sum_{r} \left(\sum_i x_{i, r}\right)^2 + P_{\text{mismatch}} \sum_{(i,r) \notin \text{Req}} x_{i, r} + P_{\text{unavail}} \sum_{r \notin \text{Avail}} x_{i, r}$$

            **Ising Spin Mapping:**
            $$x_k = \frac{I - Z_k}{2} \implies H_{\text{Ising}} = \sum_{k} h_k Z_k + \sum_{j < k} J_{jk} Z_j Z_k + \text{const}$$
            """
        )

    with q_col2:
        st.markdown("### Circuit & Telemetry Specs")
        st.markdown(
            f"""
            <div class="surface-panel">
                <div style="font-family:var(--font-mono);font-size:0.80rem;line-height:1.8;">
                    Incident Count: <strong>{n_inc_q}</strong><br>
                    Fleet Asset Count: <strong>{n_res_q}</strong><br>
                    Total Decision Variables: <strong>{total_vars}</strong><br>
                    Simulated Target Qubits: <strong>{min(12, total_vars)}</strong><br>
                    Simulator Engine: <strong>Qiskit Aer (AerSimulator)</strong><br>
                    Classical Parameter Optimizer: <strong>COBYLA</strong><br>
                    Quantum Ansatz: <strong>Parameterized QAOA (Cost + Mixer)</strong>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    # 2. Execute Quantum Experiment
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### Execute QAOA Simulation Experiment")

    e_col1, e_col2, e_col3 = st.columns(3)
    with e_col1:
        p_layers_exp = st.slider("Ansatz Depth (p layers)", 1, 3, 1, key="q_lab_p")
    with e_col2:
        shots_exp = st.select_slider("Measurement Shots", [128, 256, 512, 1024, 2048], value=512, key="q_lab_shots")
    with e_col3:
        iter_exp = st.slider("COBYLA Max Iterations", 5, 40, 15, key="q_lab_iter")

    if st.button("Run Quantum QAOA Experiment", use_container_width=True, type="primary"):
        with st.spinner("Compiling QUBO Hamiltonian and executing QAOA via Qiskit Aer..."):
            q_res = run_qaoa_optimizer(
                incidents=scen.incidents,
                resources=scen.resources,
                congestion_factor=scen.road_congestion_factor,
                p_layers=p_layers_exp,
                shots=shots_exp,
                maxiter=iter_exp,
            )
            st.session_state.current_result = q_res
            st.session_state.last_calculation_time = datetime.now().strftime("%H:%M:%S")
            st.session_state.experiment_history.append({
                "timestamp": st.session_state.last_calculation_time,
                "scenario": scen.name,
                "algorithm": q_res.algorithm_name,
                "status": q_res.status,
                "served": len(q_res.served_incident_ids),
                "unserved": len(q_res.unserved_incident_ids),
                "weighted_time": round(q_res.total_weighted_response_time, 2),
                "objective": round(q_res.objective_value, 2),
                "runtime": round(q_res.runtime_sec, 4),
            })
            st.success("Quantum QAOA simulation completed.")

    if st.session_state.current_result and "Quantum" in st.session_state.current_result.algorithm_name:
        q_out: OptimizationResult = st.session_state.current_result
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### Quantum Experiment Observables")

        meta = q_out.metadata
        qc_c1, qc_c2 = st.columns([1, 1.2])

        with qc_c1:
            st.markdown(
                f"""
                <div class="surface-panel">
                    <strong style="font-family:var(--font-mono);">CIRCUIT METRICS & OBSERVABLES:</strong>
                    <div class="divider"></div>
                    <div style="font-family:var(--font-mono);font-size:0.80rem;line-height:1.7;">
                        Qubits Evaluated: <strong>{meta.get('num_qubits')}</strong><br>
                        Compiled Circuit Depth: <strong>{meta.get('circuit_depth')} gates</strong><br>
                        QAOA Layers (p): <strong>{meta.get('p_layers')}</strong><br>
                        Optimal Gamma [γ]: <strong>{meta.get('optimal_gammas')}</strong><br>
                        Optimal Beta [β]: <strong>{meta.get('optimal_betas')}</strong><br>
                        Best Observed Bitstring: <strong>|{meta.get('best_bitstring')}⟩</strong><br>
                        Feasibility State: <strong style="color:{'#10B981' if q_out.is_feasible else '#EF4444'};">{'FEASIBLE' if q_out.is_feasible else 'INFEASIBLE'}</strong>
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with qc_c2:
            candidates = meta.get("candidate_ranking", [])
            fig_q_bar = render_quantum_distribution_chart(candidates)
            st.plotly_chart(fig_q_bar, use_container_width=True)


# ==============================================================================
# SECTION 7: ALGORITHM COMPARISON
# ==============================================================================
elif nav_page == "Algorithm Comparison":
    st.markdown("## Algorithm Comparison Benchmark")
    st.caption("Fair, side-by-side benchmark of Greedy Baseline, Classical CP-SAT, and Quantum QAOA on identical scenario parameters.")

    # Benchmark Controls
    bc1, bc2 = st.columns([1, 2])
    with bc1:
        inc_q_bench = st.checkbox("Include Quantum QAOA Simulation", value=True)
        bench_shots = st.select_slider("Quantum Shots", [256, 512, 1024], value=512) if inc_q_bench else 512
        bench_iter = st.slider("QAOA Parameter Iterations", 5, 25, 12) if inc_q_bench else 10

        if st.button("Execute Multi-Algorithm Benchmark", use_container_width=True, type="primary"):
            with st.spinner("Benchmarking Greedy, Classical CP-SAT, and Quantum QAOA on identical scenario inputs..."):
                comp = run_full_comparison(
                    incidents=scen.incidents,
                    resources=scen.resources,
                    congestion_factor=scen.road_congestion_factor,
                    include_quantum=inc_q_bench,
                    qaoa_shots=bench_shots,
                    qaoa_maxiter=bench_iter,
                )
                st.session_state.comparison_data = comp
                st.session_state.last_calculation_time = datetime.now().strftime("%H:%M:%S")
                st.success("Comparative benchmark completed.")

    with bc2:
        st.markdown(
            """
            <div class="notice-box">
                <strong>BENCHMARK SCIENTIFIC METHODOLOGY</strong><br>
                - <strong>Identical Scenario Inputs:</strong> All solvers process identical coordinates, casualty counts, and base stations.<br>
                - <strong>Standardized Objective Functions:</strong> Weighted response delay, unserved priority penalties, and vehicle costs.<br>
                - <strong>Universal Constraint Validator:</strong> Every solution is independently audited across exclusivity and capabilities.<br>
                - <strong>No Fabricated Winner:</strong> Real solver outputs are reported with exact measured numbers.
            </div>
            """,
            unsafe_allow_html=True,
        )

    if st.session_state.comparison_data:
        comp_data = st.session_state.comparison_data
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### Benchmark Performance Matrix")
        st.dataframe(comp_data["summary_df"], use_container_width=True, hide_index=True)

        fig1, fig2, fig3 = render_comparison_charts(comp_data)
        ch_c1, ch_c2 = st.columns(2)
        with ch_c1:
            st.plotly_chart(fig1, use_container_width=True)
        with ch_c2:
            st.plotly_chart(fig2, use_container_width=True)

        st.plotly_chart(fig3, use_container_width=True)


# ==============================================================================
# SECTION 8: ANALYTICS AND REPORTS
# ==============================================================================
elif nav_page == "Analytics and Reports":
    st.markdown("## Analytics & Formal Reports")
    st.caption("Comprehensive data visualization, session execution history, and audit payload export.")

    # 1. Operational Analytics Charts
    st.markdown("### Operational Analytics Suite")
    an_c1, an_c2 = st.columns(2)
    with an_c1:
        st.markdown("#### Incident Priority Matrix (Urgency vs Access Barrier)")
        fig_p_matrix = render_incident_priority_matrix(scen.incidents)
        st.plotly_chart(fig_p_matrix, use_container_width=True)

    with an_c2:
        st.markdown("#### Session Simulation Run History")
        fig_hist = render_experiment_history_chart(st.session_state.experiment_history)
        st.plotly_chart(fig_hist, use_container_width=True)

    # 2. Assemble Report Payload
    results_map = {}
    if st.session_state.comparison_data:
        results_map = st.session_state.comparison_data.get("results", {})
    elif st.session_state.current_result:
        results_map = {st.session_state.current_result.algorithm_name: st.session_state.current_result}
    else:
        greedy_auto = run_greedy_baseline(scen.incidents, scen.resources, scen.road_congestion_factor)
        results_map = {"Greedy Baseline": greedy_auto}

    payload = create_experiment_payload(scenario=scen, results=results_map)

    # 3. Export Buttons
    st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
    st.markdown("### Audit Payload Exports")

    e1, e2, e3 = st.columns(3)
    with e1:
        json_data = export_experiment_json(payload)
        st.download_button(
            label="Download Experiment JSON",
            data=json_data,
            file_name=f"{payload['experiment_id']}.json",
            mime="application/json",
            use_container_width=True,
        )
    with e2:
        csv_bundle = export_experiment_csv_bundle(payload)
        summary_csv = csv_bundle.get("algorithm_comparison.csv", "")
        st.download_button(
            label="Download Summary CSV",
            data=summary_csv,
            file_name=f"{payload['experiment_id']}_summary.csv",
            mime="text/csv",
            use_container_width=True,
        )
    with e3:
        md_text = generate_markdown_report(payload)
        st.download_button(
            label="Download Markdown Report",
            data=md_text,
            file_name=f"{payload['experiment_id']}_report.md",
            mime="text/markdown",
            use_container_width=True,
        )

    # 4. Formal Report Viewer
    with st.expander("Formal Audit Report Document", expanded=True):
        st.markdown(md_text)

    # 5. Session Execution History Table
    if st.session_state.experiment_history:
        st.markdown("<div class='divider'></div>", unsafe_allow_html=True)
        st.markdown("### Session Run Telemetry Log")
        st.dataframe(pd.DataFrame(st.session_state.experiment_history), use_container_width=True, hide_index=True)


# ==============================================================================
# SECTION 9: SETTINGS AND METHODOLOGY
# ==============================================================================
elif nav_page == "Settings and Methodology":
    st.markdown("## Methodology & System Specifications")
    st.caption("Mathematical formulation, Mixed-Integer Linear Program, QUBO derivation, and scientific disclosures.")

    st.markdown(
        r"""
        ### 1. Classical Mixed-Integer Linear Programming (MILP)
        Let $\mathcal{I} = \{1, \dots, N\}$ be the set of emergency incidents and $\mathcal{R} = \{1, \dots, M\}$ be the set of deployable response units.
        
        **Binary Decision Variables:**
        - $x_{i, r} \in \{0, 1\}$: indicates whether resource $r$ is dispatched to incident $i$.
        - $y_i \in \{0, 1\}$: indicates whether incident $i$ is fully served with all required capability types.

        **Objective Function:**
        $$\min \quad w_{\text{resp}} \sum_{i=1}^N \sum_{r=1}^M \left( \frac{\text{UrgencyScore}_i}{100} \right) c_{i, r} x_{i, r} + w_{\text{unserved}} \sum_{i=1}^N P_i (1 - y_i) + w_{\text{cost}} \sum_{i=1}^N \sum_{r=1}^M \text{Cost}_{i, r} x_{i, r}$$
        
        where:
        - $c_{i, r}$ is estimated travel transit delay in minutes.
        - $P_i = 15 \times \text{UrgencyScore}_i$ is the heavy penalty for leaving high-priority emergencies unserved.
        - $\text{Cost}_{i, r}$ is operational vehicle cost.

        **Operational Constraints:**
        1. **Resource Exclusivity:** $\sum_{i=1}^N x_{i, r} \le 1, \quad \forall r \in \mathcal{R}_{\text{available}}$
        2. **Resource Availability:** $x_{i, r} = 0, \quad \forall r \notin \mathcal{R}_{\text{available}}$
        3. **Capability Matching:** $x_{i, r} = 0, \quad \text{if } \text{Type}(r) \notin \text{RequiredTypes}(i)$
        4. **Complete Fulfillment:** $\sum_{r \in \mathcal{R}_T} x_{i, r} \ge y_i, \quad \forall T \in \text{RequiredTypes}(i)$

        ---

        ### 2. QUBO & Ising Hamiltonian Formulation
        To execute resource allocation on quantum computing architectures, constraints are encoded into an unconstrained quadratic cost function $H(x) = x^T Q x$:
        
        $$H(x) = H_{\text{transit}} - H_{\text{urgency}} + P_{\text{excl}} \sum_{r=1}^M \left( \sum_{i=1}^N x_{i, r} \right)^2 + P_{\text{mismatch}} \sum_{(i, r) \notin \text{Compat}} x_{i, r} + P_{\text{unavail}} \sum_{r \notin \text{Avail}} x_{i, r}$$
        
        By applying the standard spin transformation:
        $$x_k = \frac{1 - Z_k}{2}$$
        the problem maps directly to an **Ising Spin Glass Hamiltonian**:
        $$H_{\text{Ising}} = \sum_{k=1}^K h_k Z_k + \sum_{j < k} J_{j, k} Z_j Z_k + \text{offset}$$

        ### 3. QAOA Circuit Mechanics
        The parameterized state is prepared via alternating cost and mixer operators:
        $$|\psi(\gamma, \beta)\rangle = \prod_{l=1}^p e^{-i \beta_l H_M} e^{-i \gamma_l H_C} |+\rangle^{\otimes K}$$
        where $H_M = \sum_k X_k$ is the transverse field mixer. A classical optimizer (COBYLA) iteratively tunes $(\vec{\gamma}, \vec{\beta})$ to minimize $\langle H_C \rangle$.

        ---

        ### 4. Scientific Assumptions & Disclaimers
        > **Educational and Research Prototype:**
        > QRescue is developed as an open-source academic demonstration comparing classical integer programming against quantum approximate optimization. It is **not** a certified medical dispatch system and must not be used for real-life emergency dispatch decisions.
        """
    )
