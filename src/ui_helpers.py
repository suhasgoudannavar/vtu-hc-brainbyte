"""
UI styling and visualization engine for QRescue.
Professional Emergency Operations Center (EOC) & Quantum Lab Design System:
- Palette: #080C14 (deep canvas), #0D131E (sidebar nav), #121A26 (surface card),
           #182333 (elevated card), #1E2C40 (subtle border), #2C3E57 (border highlight),
           #F1F5F9 (primary text), #94A3B8 (secondary text), #64748B (muted text),
           #00E5FF (electric cyan), #38BDF8 (sky blue), #2563EB (cobalt accent),
           #10B981 (emerald success), #F59E0B (amber warning), #EF4444 (emergency red).
- Fonts: Inter (user interface typography), IBM Plex Mono (metrics, coordinates, telemetry).
- Aesthetic: Low-glare, high-contrast, technical credibility, mission-critical operations.
"""

from __future__ import annotations
from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

from src.data_models import Incident, Resource, Assignment, OptimizationResult, ResourceType


CUSTOM_CSS = """
<style>
    /* ==========================================================================
       QRescue Mission-Critical Operations Center Design System
       ========================================================================== */
    
    @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:ital,wght@0,400;0,500;0,600;0,700;1,400&family=Inter:wght@300;400;500;600;700;800&display=swap');

    :root {
        --bg-main: #080C14;
        --bg-nav: #0D131E;
        --bg-surface: #121A26;
        --bg-surface-elevated: #182333;
        --bg-surface-hover: #1E2A3D;
        --border-color: #223043;
        --border-subtle: #17212F;
        --border-glow: rgba(0, 229, 255, 0.25);
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
        --text-muted: #64748B;
        --accent-cyan: #00E5FF;
        --accent-cyan-dim: #00B4D8;
        --accent-blue: #38BDF8;
        --accent-cobalt: #2563EB;
        --success: #10B981;
        --warning: #F59E0B;
        --critical: #EF4444;
        --high: #F97316;
        --font-sans: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        --font-mono: 'IBM Plex Mono', ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, monospace;
    }

    /* Base Streamlit Overrides */
    .stApp {
        background-color: var(--bg-main) !important;
        color: var(--text-primary) !important;
        font-family: var(--font-sans) !important;
    }

    /* Headings */
    h1 {
        font-family: var(--font-sans) !important;
        font-size: 1.55rem !important;
        font-weight: 700 !important;
        letter-spacing: -0.02em !important;
        color: var(--text-primary) !important;
        margin-top: 0 !important;
        margin-bottom: 0.25rem !important;
    }

    h2 {
        font-family: var(--font-sans) !important;
        font-size: 1.25rem !important;
        font-weight: 600 !important;
        letter-spacing: -0.01em !important;
        color: var(--text-primary) !important;
        margin-top: 0.8rem !important;
        margin-bottom: 0.35rem !important;
    }

    h3 {
        font-family: var(--font-sans) !important;
        font-size: 1.0rem !important;
        font-weight: 600 !important;
        color: var(--text-primary) !important;
        margin-top: 0.6rem !important;
        margin-bottom: 0.35rem !important;
    }

    h4 {
        font-family: var(--font-sans) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        color: var(--text-secondary) !important;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        margin-bottom: 0.3rem !important;
    }

    p, span, label, div {
        color: var(--text-primary);
        font-size: 0.88rem;
    }

    /* Sidebar Shell Overhaul */
    section[data-testid="stSidebar"] {
        background-color: var(--bg-nav) !important;
        border-right: 1px solid var(--border-color) !important;
    }

    section[data-testid="stSidebar"] div[data-testid="stVerticalBlock"] {
        gap: 0.5rem;
    }

    /* Brand Header Box in Sidebar */
    .sidebar-brand-box {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 14px 16px;
        background: linear-gradient(135deg, rgba(0, 229, 255, 0.08) 0%, rgba(37, 99, 235, 0.05) 100%);
        border: 1px solid rgba(0, 229, 255, 0.22);
        border-radius: 6px;
        margin-bottom: 12px;
    }

    .brand-icon {
        width: 38px;
        height: 38px;
        border-radius: 6px;
        background: linear-gradient(135deg, #00E5FF 0%, #2563EB 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-family: var(--font-mono);
        font-weight: 700;
        font-size: 1.15rem;
        color: #080C14;
        box-shadow: 0 0 14px rgba(0, 229, 255, 0.4);
    }

    .brand-title {
        font-family: var(--font-sans);
        font-weight: 800;
        font-size: 1.12rem;
        letter-spacing: 0.04em;
        color: var(--text-primary);
        line-height: 1.15;
    }

    .brand-subtitle {
        font-family: var(--font-mono);
        font-size: 0.68rem;
        color: var(--accent-cyan);
        letter-spacing: 0.05em;
        text-transform: uppercase;
        margin-top: 2px;
    }

    /* Top Command Header Bar */
    .app-shell-header {
        display: flex;
        flex-wrap: wrap;
        align-items: center;
        justify-content: space-between;
        background: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 12px 18px;
        margin-bottom: 18px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.25);
    }

    .app-shell-title-group {
        display: flex;
        align-items: center;
        gap: 12px;
    }

    .app-shell-title {
        font-family: var(--font-sans);
        font-size: 1.05rem;
        font-weight: 700;
        color: var(--text-primary);
        letter-spacing: -0.01em;
    }

    .app-shell-badge {
        padding: 3px 8px;
        background: rgba(0, 229, 255, 0.12);
        border: 1px solid var(--accent-cyan);
        border-radius: 4px;
        color: var(--accent-cyan);
        font-family: var(--font-mono);
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.04em;
    }

    .app-shell-meta {
        display: flex;
        align-items: center;
        flex-wrap: wrap;
        gap: 16px;
        font-family: var(--font-mono);
        font-size: 0.78rem;
        color: var(--text-secondary);
    }

    .app-shell-meta-item {
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .app-shell-meta-item strong {
        color: var(--text-primary);
    }

    /* Live Status Indicators */
    .status-pill {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        padding: 3px 9px;
        border-radius: 4px;
        font-family: var(--font-mono);
        font-size: 0.72rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }

    .status-pill-dot {
        width: 7px;
        height: 7px;
        border-radius: 50%;
        display: inline-block;
    }

    .status-optimal {
        background: rgba(16, 185, 129, 0.14);
        border: 1px solid var(--success);
        color: var(--success);
    }
    .status-optimal .status-pill-dot {
        background: var(--success);
        box-shadow: 0 0 6px var(--success);
    }

    .status-feasible {
        background: rgba(56, 189, 248, 0.14);
        border: 1px solid var(--accent-blue);
        color: var(--accent-blue);
    }
    .status-feasible .status-pill-dot {
        background: var(--accent-blue);
        box-shadow: 0 0 6px var(--accent-blue);
    }

    .status-infeasible {
        background: rgba(239, 68, 68, 0.14);
        border: 1px solid var(--critical);
        color: var(--critical);
    }
    .status-infeasible .status-pill-dot {
        background: var(--critical);
        box-shadow: 0 0 6px var(--critical);
    }

    .status-standby {
        background: rgba(148, 163, 184, 0.12);
        border: 1px solid var(--text-muted);
        color: var(--text-secondary);
    }
    .status-standby .status-pill-dot {
        background: var(--text-muted);
    }

    /* KPI Grid & Cards */
    .kpi-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(210px, 1fr));
        gap: 12px;
        margin-bottom: 20px;
    }

    .kpi-card {
        background: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 16px 18px;
        position: relative;
        overflow: hidden;
        transition: transform 0.15s ease, border-color 0.15s ease, box-shadow 0.15s ease;
    }

    .kpi-card:hover {
        border-color: rgba(0, 229, 255, 0.35);
        box-shadow: 0 4px 18px rgba(0, 0, 0, 0.35);
    }

    .kpi-accent-bar {
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 3px;
    }
    .kpi-accent-cyan { background: linear-gradient(90deg, #00E5FF, #2563EB); }
    .kpi-accent-green { background: linear-gradient(90deg, #10B981, #059669); }
    .kpi-accent-orange { background: linear-gradient(90deg, #F97316, #EF4444); }
    .kpi-accent-red { background: linear-gradient(90deg, #EF4444, #B91C1C); }
    .kpi-accent-blue { background: linear-gradient(90deg, #38BDF8, #2563EB); }

    .kpi-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 8px;
    }

    .kpi-title {
        font-family: var(--font-mono);
        font-size: 0.72rem;
        text-transform: uppercase;
        letter-spacing: 0.06em;
        color: var(--text-secondary);
        font-weight: 500;
    }

    .kpi-icon-wrap {
        width: 26px;
        height: 26px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        justify-content: center;
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid var(--border-subtle);
    }

    .kpi-value {
        font-family: var(--font-mono);
        font-size: 1.85rem;
        font-weight: 700;
        font-variant-numeric: tabular-nums;
        color: var(--text-primary);
        line-height: 1.1;
        margin-bottom: 4px;
    }

    .kpi-subtext {
        font-size: 0.74rem;
        color: var(--text-muted);
        font-family: var(--font-sans);
        display: flex;
        align-items: center;
        gap: 6px;
    }

    .kpi-subtext strong {
        color: var(--text-secondary);
    }

    /* Surface Panel Container */
    .surface-panel {
        background: var(--bg-surface);
        border: 1px solid var(--border-color);
        border-radius: 6px;
        padding: 16px 18px;
        margin-bottom: 16px;
        box-shadow: 0 2px 10px rgba(0, 0, 0, 0.18);
    }

    .panel-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        margin-bottom: 12px;
        padding-bottom: 8px;
        border-bottom: 1px solid var(--border-subtle);
    }

    .panel-title {
        font-family: var(--font-sans);
        font-size: 0.95rem;
        font-weight: 600;
        color: var(--text-primary);
        letter-spacing: -0.01em;
    }

    /* Badges */
    .badge {
        display: inline-block;
        padding: 2px 7px;
        border-radius: 4px;
        font-family: var(--font-mono);
        font-size: 0.70rem;
        font-weight: 600;
        letter-spacing: 0.03em;
        text-transform: uppercase;
    }
    .badge-critical {
        background-color: rgba(239, 68, 68, 0.16);
        border: 1px solid var(--critical);
        color: var(--critical);
    }
    .badge-high {
        background-color: rgba(249, 115, 22, 0.16);
        border: 1px solid var(--high);
        color: var(--high);
    }
    .badge-warning {
        background-color: rgba(245, 158, 11, 0.16);
        border: 1px solid var(--warning);
        color: var(--warning);
    }
    .badge-success {
        background-color: rgba(16, 185, 129, 0.16);
        border: 1px solid var(--success);
        color: var(--success);
    }
    .badge-cyan {
        background-color: rgba(0, 229, 255, 0.14);
        border: 1px solid var(--accent-cyan);
        color: var(--accent-cyan);
    }
    .badge-neutral {
        background-color: rgba(148, 163, 184, 0.10);
        border: 1px solid var(--border-color);
        color: var(--text-secondary);
    }

    /* Buttons */
    .stButton>button {
        background: var(--bg-surface-elevated) !important;
        color: var(--text-primary) !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
        font-family: var(--font-mono) !important;
        font-size: 0.82rem !important;
        font-weight: 600 !important;
        letter-spacing: 0.02em !important;
        padding: 7px 16px !important;
        box-shadow: none !important;
        transition: all 0.15s ease !important;
    }
    .stButton>button:hover {
        background: rgba(0, 229, 255, 0.15) !important;
        color: var(--accent-cyan) !important;
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 10px rgba(0, 229, 255, 0.25) !important;
    }
    .stButton>button:focus {
        outline: 2px solid var(--accent-cyan) !important;
        outline-offset: 1px !important;
    }

    /* Primary Button */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #00E5FF 0%, #0099CC 100%) !important;
        color: #080C14 !important;
        border: 1px solid #00E5FF !important;
        font-weight: 700 !important;
        box-shadow: 0 2px 12px rgba(0, 229, 255, 0.3) !important;
    }
    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #33EBFF 0%, #00B4D8 100%) !important;
        border-color: #33EBFF !important;
        box-shadow: 0 4px 18px rgba(0, 229, 255, 0.5) !important;
        color: #080C14 !important;
    }

    /* Form Fields & Select Boxes */
    .stTextInput input, .stNumberInput input, .stSelectbox select, div[data-baseweb="select"] {
        background-color: #0A0F17 !important;
        border: 1px solid var(--border-color) !important;
        border-radius: 4px !important;
        color: var(--text-primary) !important;
        font-family: var(--font-sans) !important;
        font-size: 0.85rem !important;
    }
    .stTextInput input:focus, .stNumberInput input:focus {
        border-color: var(--accent-cyan) !important;
        box-shadow: 0 0 8px rgba(0, 229, 255, 0.2) !important;
    }

    /* DataFrames */
    div[data-testid="stDataFrame"] {
        border: 1px solid var(--border-color);
        border-radius: 6px;
        background: var(--bg-surface);
        font-family: var(--font-mono);
        font-size: 0.80rem;
    }

    /* Notice and Callout Boxes */
    .notice-box {
        background: rgba(0, 229, 255, 0.04);
        border-left: 3px solid var(--accent-cyan);
        border-top: 1px solid var(--border-color);
        border-right: 1px solid var(--border-color);
        border-bottom: 1px solid var(--border-color);
        border-radius: 0 6px 6px 0;
        padding: 10px 14px;
        font-size: 0.82rem;
        color: var(--text-secondary);
        margin: 10px 0 16px 0;
        line-height: 1.5;
    }

    .notice-box strong {
        color: var(--text-primary);
        font-family: var(--font-mono);
        font-size: 0.80rem;
    }

    /* Precision Divider */
    .divider {
        height: 1px;
        background: var(--border-color);
        margin: 14px 0;
    }

    .mono {
        font-family: var(--font-mono) !important;
        font-variant-numeric: tabular-nums;
    }

    /* Navigation Radio Items in Sidebar */
    div[data-testid="stRadio"] > div {
        gap: 4px;
    }

    div[data-testid="stRadio"] label {
        background: rgba(18, 26, 38, 0.6);
        border: 1px solid var(--border-subtle);
        border-radius: 5px;
        padding: 7px 12px;
        font-family: var(--font-sans);
        font-size: 0.84rem;
        font-weight: 500;
        color: var(--text-secondary);
        transition: all 0.15s ease;
        margin-bottom: 2px;
    }

    div[data-testid="stRadio"] label:hover {
        background: rgba(0, 229, 255, 0.08);
        border-color: rgba(0, 229, 255, 0.3);
        color: var(--text-primary);
    }
</style>
"""


# ------------------------------------------------------------------------------
# 1. Spatial Simulation Map (Schematic 2D Tactical Operations Map)
# ------------------------------------------------------------------------------
def render_spatial_simulation_map(
    incidents: List[Incident],
    resources: List[Resource],
    assignments: Optional[List[Assignment]] = None,
    show_incidents: bool = True,
    show_resources: bool = True,
    show_routes: bool = True,
    selected_incident_id: Optional[str] = None,
    selected_resource_id: Optional[str] = None,
) -> go.Figure:
    """
    Renders an operational 2D tactical cartography map.
    Styled with the EOC dark theme:
    - Background: #080C14 canvas, #121A26 surface, #1E2C40 grid lines.
    - Incidents: Severity-coded circles with casualty sizing and selection halos.
    - Resources: Distinct tactical markers by classification (Ambulance, Rescue, Fire, Medical).
    - Dispatch Vectors: Cyan solid vectors for full fulfillment, dashed amber for partial.
    """
    fig = go.Figure()
    
    resource_map = {r.id: r for r in resources}
    incident_map = {i.id: i for i in incidents}
    
    # 1. Allocation Vector Lines
    if show_routes and assignments:
        for asgn in assignments:
            inc = incident_map.get(asgn.incident_id)
            if not inc:
                continue
            for rid in asgn.resource_ids:
                res = resource_map.get(rid)
                if not res:
                    continue
                is_selected = (asgn.incident_id == selected_incident_id) or (rid == selected_resource_id)
                line_color = "#00E5FF" if asgn.is_fully_served else "#F59E0B"
                line_width = 2.8 if is_selected else 1.6
                line_dash = "solid" if asgn.is_fully_served else "dot"
                
                fig.add_trace(
                    go.Scatter(
                        x=[res.lon, inc.lon],
                        y=[res.lat, inc.lat],
                        mode="lines",
                        line=dict(color=line_color, width=line_width, dash=line_dash),
                        hoverinfo="text",
                        hovertext=(
                            f"<b>DISPATCH VECTOR</b><br>"
                            f"Asset: {res.name} [{res.id}]<br>"
                            f"Target: {inc.name} [{inc.id}]<br>"
                            f"Transit Time: {asgn.estimated_travel_time_min:.1f} min<br>"
                            f"Coverage: {'FULFILLED' if asgn.is_fully_served else 'PARTIAL'}"
                        ),
                        showlegend=False,
                    )
                )

    # 2. Simulated Incidents Layer
    if show_incidents and incidents:
        sev_colors = {
            5: "#EF4444",  # Critical (Red)
            4: "#F97316",  # High (Orange)
            3: "#F59E0B",  # Moderate (Amber)
            2: "#10B981",  # Minor (Green)
            1: "#64748B",  # Routine (Muted)
        }
        
        inc_lats = [i.lat for i in incidents]
        inc_lons = [i.lon for i in incidents]
        inc_texts = [
            f"<b>INCIDENT [{i.id}]</b><br>"
            f"Event: {i.name}<br>"
            f"Hazard: {i.category}<br>"
            f"Severity: {i.severity}/5 ({i.priority_category.upper()})<br>"
            f"Casualties: {i.people_affected}<br>"
            f"Urgency Score: {i.urgency_score:.1f} / 100<br>"
            f"Required Fleet: {', '.join(i.required_resource_types)}<br>"
            f"Terrain Barrier: {i.access_difficulty:.1f}x"
            for i in incidents
        ]
        inc_colors = [sev_colors.get(i.severity, "#EF4444") for i in incidents]
        inc_sizes = [
            24 if i.id == selected_incident_id else max(11, min(22, 9 + int(i.people_affected / 12)))
            for i in incidents
        ]
        inc_borders = [
            "#00E5FF" if i.id == selected_incident_id else "#F1F5F9"
            for i in incidents
        ]
        inc_border_widths = [3.0 if i.id == selected_incident_id else 1.2 for i in incidents]

        fig.add_trace(
            go.Scatter(
                x=inc_lons,
                y=inc_lats,
                mode="markers+text",
                marker=dict(
                    size=inc_sizes,
                    color=inc_colors,
                    symbol="circle",
                    line=dict(color=inc_borders, width=inc_border_widths),
                    opacity=0.92,
                ),
                text=[f" {i.id}" for i in incidents],
                textposition="top right",
                textfont=dict(family="IBM Plex Mono, monospace", size=9, color="#F1F5F9"),
                hoverinfo="text",
                hovertext=inc_texts,
                name="Incidents (Triage Targets)",
            )
        )

    # 3. Fleet Assets Layer (Distinct Symbols by Classification)
    if show_resources and resources:
        # Group resources by type for distinct iconography
        symbol_map = {
            ResourceType.AMBULANCE.value: "cross",
            ResourceType.RESCUE_TEAM.value: "diamond",
            ResourceType.FIRE_RESPONSE_TEAM.value: "square",
            ResourceType.MEDICAL_SUPPLY_UNIT.value: "triangle-up",
        }
        
        for rtype_val in [t.value for t in ResourceType]:
            sub_res = [r for r in resources if r.resource_type == rtype_val]
            if not sub_res:
                continue
                
            res_lats = [r.lat for r in sub_res]
            res_lons = [r.lon for r in sub_res]
            res_colors = ["#38BDF8" if r.available else "#64748B" for r in sub_res]
            res_symbols = [symbol_map.get(rtype_val, "square") if r.available else "x" for r in sub_res]
            res_sizes = [19 if r.id == selected_resource_id else 12 for r in sub_res]
            res_borders = ["#00E5FF" if r.id == selected_resource_id else "#080C14" for r in sub_res]
            res_texts = [
                f"<b>ASSET [{r.id}]</b><br>"
                f"Designation: {r.name}<br>"
                f"Type: {r.resource_type}<br>"
                f"Readiness: {'OPERATIONAL (AVAILABLE)' if r.available else 'MAINTENANCE / OFFLINE'}<br>"
                f"Speed: {r.response_speed_kmh} km/h | Capacity: {r.capacity} persons<br>"
                f"Operating Cost: ${r.operating_cost_per_hour}/hr"
                for r in sub_res
            ]

            fig.add_trace(
                go.Scatter(
                    x=res_lons,
                    y=res_lats,
                    mode="markers+text",
                    marker=dict(
                        size=res_sizes,
                        color=res_colors,
                        symbol=res_symbols,
                        line=dict(color=res_borders, width=1.5),
                    ),
                    text=[f" {r.id}" for r in sub_res],
                    textposition="bottom left",
                    textfont=dict(family="IBM Plex Mono, monospace", size=8.5, color="#38BDF8"),
                    hoverinfo="text",
                    hovertext=res_texts,
                    name=f"Fleet: {rtype_val}",
                )
            )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono, monospace", size=10, color="#94A3B8"),
        xaxis=dict(
            title=dict(text="SYNTHETIC LONGITUDE", font=dict(size=9, color="#64748B")),
            showgrid=True,
            gridcolor="#1E2C40",
            zeroline=False,
            tickfont=dict(size=9, color="#64748B"),
        ),
        yaxis=dict(
            title=dict(text="SYNTHETIC LATITUDE", font=dict(size=9, color="#64748B")),
            showgrid=True,
            gridcolor="#1E2C40",
            zeroline=False,
            scaleanchor="x",
            scaleratio=1,
            tickfont=dict(size=9, color="#64748B"),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.01,
            xanchor="left",
            x=0,
            bgcolor="rgba(18, 26, 38, 0.92)",
            bordercolor="#223043",
            borderwidth=1,
            font=dict(size=8.5, color="#F1F5F9"),
        ),
        margin=dict(l=35, r=35, t=35, b=35),
        height=480,
    )
    return fig


# ------------------------------------------------------------------------------
# 2. Incident Severity Distribution Chart
# ------------------------------------------------------------------------------
def render_incident_severity_chart(incidents: List[Incident]) -> go.Figure:
    """
    Renders an interactive horizontal bar chart of incident counts grouped by Severity.
    """
    levels = ["Critical (5)", "High (4)", "Moderate (3)", "Minor (2)", "Routine (1)"]
    counts = {5: 0, 4: 0, 3: 0, 2: 0, 1: 0}
    for inc in incidents:
        counts[inc.severity] = counts.get(inc.severity, 0) + 1

    y_vals = ["Critical (5)", "High (4)", "Moderate (3)", "Minor (2)", "Routine (1)"]
    x_vals = [counts[5], counts[4], counts[3], counts[2], counts[1]]
    colors = ["#EF4444", "#F97316", "#F59E0B", "#10B981", "#64748B"]

    fig = go.Figure(
        go.Bar(
            x=x_vals,
            y=y_vals,
            orientation="h",
            marker=dict(color=colors, line=dict(color="#080C14", width=1)),
            text=[f" {c} inc." if c > 0 else "" for c in x_vals],
            textposition="inside",
            textfont=dict(family="IBM Plex Mono", size=10, color="#FFFFFF"),
            hoverinfo="y+x",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        margin=dict(l=20, r=20, t=30, b=20),
        height=220,
        xaxis=dict(title="Active Emergencies", showgrid=True, gridcolor="#1E2C40", dtick=1),
        yaxis=dict(autorange="reversed"),
    )
    return fig


# ------------------------------------------------------------------------------
# 3. Resource Utilization Doughnut Chart
# ------------------------------------------------------------------------------
def render_resource_utilization_chart(
    resources: List[Resource],
    assignments: Optional[List[Assignment]] = None,
) -> go.Figure:
    """
    Renders a clean doughnut chart showing fleet operational status:
    - Assigned (Dispatched)
    - Available (Standby Readiness)
    - Unavailable (Maintenance / Offline)
    """
    assigned_ids = set()
    if assignments:
        for asgn in assignments:
            assigned_ids.update(asgn.resource_ids)

    n_assigned = sum(1 for r in resources if r.id in assigned_ids and r.available)
    n_available = sum(1 for r in resources if r.id not in assigned_ids and r.available)
    n_offline = sum(1 for r in resources if not r.available)

    labels = ["Dispatched", "Standby Readiness", "Maintenance / Offline"]
    values = [n_assigned, n_available, n_offline]
    colors = ["#00E5FF", "#10B981", "#64748B"]

    fig = go.Figure(
        go.Pie(
            labels=labels,
            values=values,
            hole=0.62,
            marker=dict(colors=colors, line=dict(color="#121A26", width=2)),
            textinfo="value+percent",
            textfont=dict(family="IBM Plex Mono", size=10, color="#F1F5F9"),
            hoverinfo="label+value+percent",
        )
    )

    total_units = len(resources)
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        margin=dict(l=10, r=10, t=25, b=10),
        height=220,
        showlegend=True,
        legend=dict(orientation="h", y=-0.15, x=0.0, font=dict(size=8.5)),
        annotations=[
            dict(
                text=f"<b>{total_units}</b><br><span style='font-size:8px;color:#64748B;'>FLEET</span>",
                x=0.5,
                y=0.5,
                font=dict(size=14, color="#F1F5F9", family="IBM Plex Mono"),
                showarrow=False,
            )
        ],
    )
    return fig


# ------------------------------------------------------------------------------
# 4. Response Time Analysis Chart
# ------------------------------------------------------------------------------
def render_response_time_analysis_chart(
    assignments: List[Assignment],
    incidents: List[Incident],
) -> go.Figure:
    """
    Renders an interactive bar chart of estimated transit & total service duration per incident,
    color-coded by incident severity.
    """
    if not assignments:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#121A26",
            plot_bgcolor="#080C14",
            height=260,
            annotations=[dict(text="No active assignment manifest. Run simulation to calculate response times.", showarrow=False, font=dict(color="#64748B"))],
        )
        return fig

    inc_map = {i.id: i for i in incidents}
    data = []
    for asgn in assignments:
        inc = inc_map.get(asgn.incident_id)
        if not inc:
            continue
        data.append({
            "Incident": inc.id,
            "Name": inc.name,
            "TransitTime": asgn.estimated_travel_time_min,
            "ServiceDuration": asgn.total_response_time_min,
            "Severity": inc.severity,
            "Served": asgn.is_fully_served,
        })

    df = pd.DataFrame(data)
    if df.empty:
        fig = go.Figure()
        fig.update_layout(template="plotly_dark", paper_bgcolor="#121A26", height=260)
        return fig

    sev_palette = {5: "#EF4444", 4: "#F97316", 3: "#F59E0B", 2: "#10B981", 1: "#64748B"}
    bar_colors = [sev_palette.get(s, "#00E5FF") for s in df["Severity"]]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=df["Incident"],
            y=df["TransitTime"],
            name="Estimated Transit Delay (min)",
            marker=dict(color=bar_colors, line=dict(color="#080C14", width=1)),
            hovertext=[f"<b>{row['Incident']}</b>: {row['Name']}<br>Transit: {row['TransitTime']:.1f} min<br>Severity: {row['Severity']}/5" for _, row in df.iterrows()],
            hoverinfo="text",
        )
    )

    # Reference line for mean transit time
    mean_transit = df["TransitTime"].mean()
    if not np.isnan(mean_transit) and mean_transit > 0:
        fig.add_hline(
            y=mean_transit,
            line_dash="dot",
            line_color="#00E5FF",
            annotation_text=f"Mean Transit: {mean_transit:.1f}m",
            annotation_position="top right",
            annotation_font=dict(family="IBM Plex Mono", size=9, color="#00E5FF"),
        )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        height=260,
        margin=dict(l=30, r=25, t=30, b=30),
        xaxis=dict(title="Incident Target", gridcolor="#1E2C40"),
        yaxis=dict(title="Transit Minutes", gridcolor="#1E2C40"),
    )
    return fig


# ------------------------------------------------------------------------------
# 5. Incident Priority Matrix (Bubble / Scatter Plot)
# ------------------------------------------------------------------------------
def render_incident_priority_matrix(incidents: List[Incident]) -> go.Figure:
    """
    Renders an interactive Priority Matrix:
    - X: Terrain Access Difficulty
    - Y: Priority / Urgency Score (0 - 100)
    - Bubble Size: Casualties / Affected Persons
    - Color: Severity
    """
    sev_map = {5: "#EF4444", 4: "#F97316", 3: "#F59E0B", 2: "#10B981", 1: "#64748B"}
    
    fig = go.Figure()
    for inc in incidents:
        fig.add_trace(
            go.Scatter(
                x=[inc.access_difficulty],
                y=[inc.urgency_score],
                mode="markers+text",
                marker=dict(
                    size=max(12, min(36, 10 + int(inc.people_affected / 8))),
                    color=sev_map.get(inc.severity, "#00E5FF"),
                    line=dict(color="#F1F5F9", width=1),
                    opacity=0.88,
                ),
                text=[inc.id],
                textposition="top center",
                textfont=dict(family="IBM Plex Mono", size=8.5, color="#F1F5F9"),
                hoverinfo="text",
                hovertext=(
                    f"<b>{inc.id} - {inc.name}</b><br>"
                    f"Urgency Score: {inc.urgency_score:.1f} / 100<br>"
                    f"Severity Level: {inc.severity} / 5<br>"
                    f"Casualties: {inc.people_affected}<br>"
                    f"Terrain Barrier: {inc.access_difficulty:.2f}x<br>"
                    f"Required: {', '.join(inc.required_resource_types)}"
                ),
                showlegend=False,
            )
        )

    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        height=280,
        margin=dict(l=35, r=25, t=30, b=35),
        xaxis=dict(title="Terrain Access Barrier Multiplier", gridcolor="#1E2C40"),
        yaxis=dict(title="Priority Urgency Score (0-100)", gridcolor="#1E2C40", range=[0, 105]),
    )
    return fig


# ------------------------------------------------------------------------------
# 6. Algorithm Comparison Charts
# ------------------------------------------------------------------------------
def render_comparison_charts(comparison_data: Dict[str, Any]) -> Tuple[go.Figure, go.Figure, go.Figure]:
    """
    Renders 3 multi-metric analytical benchmark comparison charts:
    - Chart 1: Fulfillment Audit (Served vs. Unserved Stacked Bars)
    - Chart 2: Objective Value & Execution Runtime (Dual Axis)
    - Chart 3: Mean Estimated Response Time Comparison
    """
    summary_df: pd.DataFrame = comparison_data["summary_df"]
    
    # 1. Incident Fulfillment Audit
    fig1 = go.Figure()
    fig1.add_trace(
        go.Bar(
            name="Served Incidents",
            x=summary_df["Algorithm"],
            y=summary_df["Served Incidents"],
            marker_color="#00E5FF",
            marker_line=dict(color="#080C14", width=1),
            text=summary_df["Served Incidents"],
            textposition="auto",
            textfont=dict(family="IBM Plex Mono", size=10, color="#080C14"),
        )
    )
    fig1.add_trace(
        go.Bar(
            name="Unserved Incidents",
            x=summary_df["Algorithm"],
            y=summary_df["Unserved Incidents"],
            marker_color="#EF4444",
            marker_line=dict(color="#080C14", width=1),
            text=summary_df["Unserved Incidents"],
            textposition="auto",
            textfont=dict(family="IBM Plex Mono", size=10, color="#FFFFFF"),
        )
    )
    fig1.update_layout(
        title=dict(
            text="INCIDENT FULFILLMENT AUDIT (SERVED VS. UNSERVED)",
            font=dict(family="IBM Plex Mono", size=10, color="#F1F5F9"),
        ),
        barmode="stack",
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        height=280,
        margin=dict(l=30, r=25, t=45, b=25),
        yaxis=dict(title="Count", gridcolor="#1E2C40"),
        xaxis=dict(gridcolor="#1E2C40"),
        legend=dict(orientation="h", y=1.14, x=0, bgcolor="rgba(18, 26, 38, 0.85)"),
    )

    # 2. Objective Value & Runtime
    fig2 = go.Figure()
    fig2.add_trace(
        go.Bar(
            name="Objective Score (Minimization)",
            x=summary_df["Algorithm"],
            y=summary_df["Objective Value"],
            marker_color="#182333",
            marker_line=dict(color="#00E5FF", width=1.5),
        )
    )
    fig2.add_trace(
        go.Scatter(
            name="Execution Runtime (sec)",
            x=summary_df["Algorithm"],
            y=summary_df["Runtime (sec)"],
            yaxis="y2",
            mode="lines+markers",
            marker=dict(color="#F59E0B", size=8, symbol="diamond"),
            line=dict(color="#F59E0B", width=2),
        )
    )
    fig2.update_layout(
        title=dict(
            text="OBJECTIVE VALUE & SOLVER RUNTIME",
            font=dict(family="IBM Plex Mono", size=10, color="#F1F5F9"),
        ),
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        height=280,
        margin=dict(l=30, r=30, t=45, b=25),
        yaxis=dict(title="Objective Score", gridcolor="#1E2C40"),
        yaxis2=dict(
            title=dict(text="Runtime (s)", font=dict(color="#F59E0B")),
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(color="#F59E0B"),
        ),
        xaxis=dict(gridcolor="#1E2C40"),
        legend=dict(orientation="h", y=1.14, x=0, bgcolor="rgba(18, 26, 38, 0.85)"),
    )

    # 3. Mean Transit Time Comparison
    resp_col = "Weighted Resp Time (min)" if "Weighted Resp Time (min)" in summary_df.columns else "Total Weighted Response Time (min)"
    fig3 = go.Figure()
    fig3.add_trace(
        go.Bar(
            name="Weighted Transit Delay (min)",
            x=summary_df["Algorithm"],
            y=summary_df[resp_col],
            marker_color="#38BDF8",
            marker_line=dict(color="#080C14", width=1),
        )
    )
    fig3.update_layout(
        title=dict(
            text="WEIGHTED RESPONSE TIME COMPARISON",
            font=dict(family="IBM Plex Mono", size=10, color="#F1F5F9"),
        ),
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        height=280,
        margin=dict(l=30, r=25, t=45, b=25),
        yaxis=dict(title="Minutes", gridcolor="#1E2C40"),
        xaxis=dict(gridcolor="#1E2C40"),
    )

    return fig1, fig2, fig3


# ------------------------------------------------------------------------------
# 7. Quantum Sampling Distribution Chart
# ------------------------------------------------------------------------------
def render_quantum_distribution_chart(candidate_ranking: List[Dict[str, Any]]) -> go.Figure:
    """
    Renders the quantum sampling probability distribution of QAOA measured bitstrings.
    """
    if not candidate_ranking:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#121A26",
            plot_bgcolor="#080C14",
            height=240,
            annotations=[dict(text="No quantum distribution available. Run QAOA in Quantum Lab.", showarrow=False, font=dict(color="#64748B"))],
        )
        return fig

    top_candidates = candidate_ranking[:8]
    cdf = pd.DataFrame(top_candidates)
    
    # Color feasible vs infeasible bitstrings
    bar_colors = ["#10B981" if c.get("is_feasible", False) else "#64748B" for c in top_candidates]

    fig = go.Figure(
        go.Bar(
            x=cdf["bitstring"],
            y=cdf["probability"],
            marker=dict(color=bar_colors, line=dict(color="#080C14", width=1)),
            hovertext=[f"Bitstring: |{r['bitstring']}⟩<br>Prob: {r['probability']*100:.1f}%<br>Cost: {r['cost']:.2f}<br>Feasible: {r['is_feasible']}" for _, r in cdf.iterrows()],
            hoverinfo="text",
        )
    )

    fig.update_layout(
        title=dict(
            text="QAOA MEASURED BITSTRING SAMPLING DISTRIBUTION (|x⟩)",
            font=dict(family="IBM Plex Mono", size=10, color="#F1F5F9"),
        ),
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        height=240,
        margin=dict(l=25, r=25, t=40, b=25),
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        yaxis=dict(title="Probability", gridcolor="#1E2C40"),
        xaxis=dict(title="Quantum State |x⟩", gridcolor="#1E2C40"),
    )
    return fig


# ------------------------------------------------------------------------------
# 8. Session Experiment History Chart
# ------------------------------------------------------------------------------
def render_experiment_history_chart(experiment_history: List[Dict[str, Any]]) -> go.Figure:
    """
    Renders timeline of previous simulation runs across the session.
    """
    if not experiment_history:
        fig = go.Figure()
        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#121A26",
            plot_bgcolor="#080C14",
            height=240,
            annotations=[dict(text="No session history recorded yet. Run simulations to log benchmarks.", showarrow=False, font=dict(color="#64748B"))],
        )
        return fig

    hdf = pd.DataFrame(experiment_history)
    fig = go.Figure()
    
    # Run markers
    x_indices = [f"Run {i+1} ({r['algorithm'][:8]})" for i, r in hdf.iterrows()]
    fig.add_trace(
        go.Bar(
            x=x_indices,
            y=hdf["served"],
            name="Served Incidents",
            marker_color="#00E5FF",
        )
    )
    fig.add_trace(
        go.Scatter(
            x=x_indices,
            y=hdf["objective"],
            name="Objective Score",
            yaxis="y2",
            mode="lines+markers",
            marker=dict(color="#F59E0B", size=8),
            line=dict(color="#F59E0B", width=2),
        )
    )

    fig.update_layout(
        title=dict(
            text="SESSION SIMULATION RUN TIMELINE",
            font=dict(family="IBM Plex Mono", size=10, color="#F1F5F9"),
        ),
        template="plotly_dark",
        plot_bgcolor="#080C14",
        paper_bgcolor="#121A26",
        font=dict(family="IBM Plex Mono", size=9, color="#94A3B8"),
        height=240,
        margin=dict(l=30, r=30, t=40, b=25),
        yaxis=dict(title="Served Count", gridcolor="#1E2C40"),
        yaxis2=dict(
            title=dict(text="Objective Value", font=dict(color="#F59E0B")),
            overlaying="y",
            side="right",
            showgrid=False,
            tickfont=dict(color="#F59E0B"),
        ),
        xaxis=dict(gridcolor="#1E2C40"),
        legend=dict(orientation="h", y=1.14, x=0, bgcolor="rgba(18, 26, 38, 0.85)"),
    )
    return fig
