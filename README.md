# 🚨 QRescue: AI-Powered Disaster Response Using Quantum Optimization

[![Python](https://img.shields.io/badge/Python-3.11%20%7C%203.12-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42+-FF4B4B.svg)](https://streamlit.io/)
[![Google OR-Tools](https://img.shields.io/badge/OR--Tools-CP--SAT-4285F4.svg)](https://developers.google.com/optimization)
[![Qiskit](https://img.shields.io/badge/Qiskit-2.0+-6929C4.svg)](https://qiskit.org/)
[![Qiskit Aer](https://img.shields.io/badge/Qiskit%20Aer-Simulator-8A3FFC.svg)](https://github.com/Qiskit/qiskit-aer)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Tests](https://img.shields.io/badge/Tests-25%20Passing-brightgreen.svg)]()

> **Educational & Research Prototype:** QRescue is a functional simulation and optimization platform designed for research and educational purposes. It explores the intersection of classical combinatorial optimization and quantum approximate optimization (QAOA) for disaster logistics. It is **not** a validated emergency dispatch system.

---

## 📌 Problem Statement
During large-scale natural and technological disasters (floods, landslides, structural collapses, multi-hazard fires), emergency response coordinators face severe operational challenges:
- Multiple emergencies compete for limited specialized resources (ambulances, swiftwater rescue squads, fire engines, trauma units).
- Ad-hoc dispatch or greedy nearest-neighbor heuristics cause severe bottlenecks—allocating specialized heavy rescue units to low-priority incidents while catastrophic emergencies remain unserved.
- Road congestion, collapsed bridges, and debris slow travel times unpredictably.

---

## 💡 The QRescue Solution
**QRescue** provides an end-to-end decision-support simulation platform:
1. **Multi-Factor Incident Triage:** Prioritizes incidents based on casualty count, severity ($1-5$), time sensitivity, access difficulty, and disaster category.
2. **Realistic Response-Time Estimation:** Employs Haversine distance with a $1.35\times$ road curvature factor, nominal fleet speeds, and weather/traffic congestion multipliers.
3. **Classical Constraint Optimization:** Solves the multi-resource allocation problem globally using **Google OR-Tools CP-SAT**, enforcing zero resource conflicts and strict capability matching.
4. **Quantum Optimization (QAOA):** Maps the allocation problem to a **QUBO** and **Ising spin Hamiltonian**, simulating the **Quantum Approximate Optimization Algorithm (QAOA)** with **Qiskit** and **Qiskit Aer**.
5. **Universal Constraint Verification:** Independently audits every solution across exclusivity, availability, and capability requirements.
6. **Side-by-Side Benchmarking:** Compares Greedy Baseline, Classical CP-SAT, and Quantum QAOA on identical scenario parameters.
7. **One-Click Audit Export:** Generates reproducible JSON payloads, CSV bundles, and Markdown reports.

---

## 🏗️ System Architecture

```mermaid
graph TD
    subgraph Data & Simulation
        Scenarios[Disaster Scenarios<br/>Flood, Landslide, Multi-Hazard]
        Triage[Triage Engines<br/>Mode A: Formula | Mode B: Random Forest ML]
        Travel[Travel Modeling<br/>Curvature Factor + Congestion Multiplier]
    end

    subgraph Optimization Engines
        Greedy[Greedy Baseline Heuristic]
        Classical[Google OR-Tools CP-SAT Optimizer]
        QUBO[QUBO Formulation & Ising Mapping]
        Quantum[Qiskit QAOA Circuit & Aer Simulation]
    end

    subgraph Validation & UI
        Checker[Universal Constraint Validator]
        UI[Streamlit Operations Dashboard]
        Reports[Export Engine: JSON, CSV, Markdown]
    end

    Scenarios --> Triage
    Scenarios --> Travel
    Triage --> Greedy
    Triage --> Classical
    Triage --> QUBO
    Travel --> Greedy
    Travel --> Classical
    Travel --> QUBO
    QUBO --> Quantum

    Greedy --> Checker
    Classical --> Checker
    Quantum --> Checker

    Checker --> UI
    Checker --> Reports
```

---

## 🛠️ Free & Open-Source Technology Stack

| Component | Library / Framework | Purpose |
| :--- | :--- | :--- |
| **Language** | Python 3.11 / 3.12 | Core logic & algorithms |
| **Dashboard** | Streamlit | Professional dark-navy operations UI |
| **Classical Solver** | Google OR-Tools (CP-SAT) | Exact mixed-integer constraint optimization |
| **Quantum Framework** | Qiskit & Qiskit Aer | QUBO formulation, Ising Hamiltonian, QAOA simulation |
| **Machine Learning** | Scikit-Learn | Supervised triage model experiment & feature evaluation |
| **Data & Math** | Pandas, NumPy, SciPy | Matrix operations, COBYLA optimization, tabular analytics |
| **Visualization** | Plotly | Interactive geospatial 2D maps and benchmark charts |
| **Testing** | Pytest | Comprehensive test suite (25 unit & integration tests) |

*100% free and open-source. Requires zero paid APIs, zero cloud credits, and runs completely locally and offline.*

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone <your-repository-url>
cd QRescue
```

### 2. Set Up a Virtual Environment
```bash
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# macOS / Linux
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Streamlit Dashboard
```bash
streamlit run app.py
```
Open your browser to `http://localhost:8501`.

---

## 🧪 Running the Test Suite
The project includes 25 unit and integration tests covering data models, validation, response time estimation, classical optimization, QUBO construction, QAOA execution, and reporting:

```bash
pytest -v
```

Output:
```text
============================= 25 passed in 5.72s ==============================
```

---

## 👥 Hackathon Team Division of Work (4 Members)

| Team Member | Domain / Responsibilities | Deliverables |
| :--- | :--- | :--- |
| **Member 1: AI/ML & Prioritization** | Incident data models, baseline scoring formula, synthetic dataset generation, Random Forest classifier, feature importance evaluation. | `src/data_models.py`, `src/prioritization.py`, `tests/test_prioritization.py` |
| **Member 2: Classical Optimization** | Response-time estimation model, road curvature factor, Google OR-Tools CP-SAT formulation, greedy baseline, and constraint validation engine. | `src/response_time.py`, `src/classical_optimizer.py`, `tests/test_classical_optimizer.py` |
| **Member 3: Quantum Optimization** | QUBO mathematical formulation, penalty multiplier tuning, Ising Hamiltonian conversion (`SparsePauliOp`), QAOA circuit assembly, and Qiskit Aer simulation. | `src/qubo_model.py`, `src/quantum_optimizer.py`, `tests/test_qubo_and_quantum.py`, `docs/methodology.md` |
| **Member 4: UI/UX, Integration & Lead** | Streamlit multi-page dashboard, Plotly geospatial maps, dark navy styling, algorithm benchmark integration, export engine, demo script, and documentation. | `app.py`, `src/ui_helpers.py`, `src/evaluation.py`, `src/reporting.py`, `docs/demo_script.md` |

---

## 🔬 Scientific Honesty & Limitations
- **Quantum Advantage Disclosure:** QRescue does **not** claim quantum advantage. Current NISQ devices and local CPU quantum simulators incur exponential classical matrix overhead ($O(2^N)$). Classical CP-SAT solvers are significantly faster for current operational problem sizes.
- **Hardware Realism:** The quantum experiment runs on **Qiskit Aer** (CPU statevector/shot-based simulation), **not** physical quantum processors.
- **Synthetic Data:** Coordinates, road topologies, and incident attributes are synthetic simulations designed to test optimization performance.
- **Div-by-Zero Protection:** Percentage improvement formulas strictly check that baseline costs are positive before calculation.

---

## 📤 Git Repository Initialization
To push this project to your own GitHub account:

```bash
git init
git add .
git commit -m "feat: Initial release of QRescue disaster optimization platform"
git branch -M main
git remote add origin https://github.com/<your-username>/QRescue.git
git push -u origin main
```

---

## 📄 License
This project is open-source under the [MIT License](LICENSE).
